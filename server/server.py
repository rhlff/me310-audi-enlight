from flask import Flask, render_template, request, g

from led_controller import LEDController
from led_controller.led_world import LEDWorldBuilder, ObjectLocation
from led_controller.led_objects import LEDSpot, LEDContinuousDrop
import opc


app = Flask(__name__)
FC_SERVER = '172.16.20.233:7890'
# FC_SERVER = '192.168.2.1:7890'

import signal
import sys

def signal_handler(signal, frame):
        teardown_led_controller()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

led_controller = None
working_light_led = None

settings = [
    { 'name': 'Working Light', 'url': 'working_light', 'activated': False },
    { 'name': 'Beat Detection', 'url': None, 'activated': False },
]

def toggle_working_light(activate):
    global working_light_led
    if activate:
        if working_light_led is None:
            color = (237, 183, 21)
            location = ObjectLocation(-45, 90)
            working_light_led = LEDSpot(color, location, 120)
            get_led_controller().add_symbol(working_light_led)
    else:
        if working_light_led is not None:
            get_led_controller().remove_symbol(working_light_led)
            working_light_led = None

def get_led_controller():
    global led_controller
    if led_controller is None:
        world = LEDWorldBuilder().add_octa_circle().build()
        client = opc.Client(FC_SERVER)
        led_controller = LEDController(world, client)
        led_controller.start()
        led_controller.off()
    return led_controller

def teardown_led_controller():
    global led_controller
    if led_controller is not None:
        led_controller.stop()

@app.route('/')
def dashboard():
    return render_template('dashboard.html', settings=settings)

@app.route('/toggle', methods=['POST'])
def toggle_settings():
    global settings
    setting = next( (s for s in settings if s['name'] == request.form['name'] ), None)
    if setting is not None:
        idx = settings.index(setting)
        setting['activated'] = settings[idx]['activated'] = (request.form['activate'] == 'true')
        if setting['name'] == 'Working Light':
            toggle_working_light(setting['activated'])
    return ('', 204)

@app.route('/working-light')
def working_light():
    return render_template('working_light.html')

@app.route('/beat', methods=['POST'])
def receive_beat():
    global settings
    setting = next( (s for s in settings if s['name'] == 'Beat Detection' ), None)
    if setting and setting['activated'] and float(request.form['energy']) > 1.5:
        location = ObjectLocation(0, 0.5)
        color = (52, 141, 151)
        led_drop = LEDContinuousDrop(color, location, 0.75, period=0.1, end_after=1)
        get_led_controller().add_symbol(led_drop)
    return ('', 204)
