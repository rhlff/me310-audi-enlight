from flask import Flask, render_template, request
import signal
import sys

from leds import get_led_controller, teardown_led_controller
from led_controller.led_world import ObjectLocation
from led_controller.led_objects import LEDSpot
from blueprints.working_light import working_light
from blueprints.beat_detection import beat_detection
from blueprints.bike import testing_bike
from blueprints.parking import testing_parking
from blueprints.alarm import testing_alarm
from blueprints.emergency import emergency
import thread
import time


app = Flask(__name__)


blueprints = [working_light, beat_detection, testing_bike, testing_parking, testing_alarm, emergency]
for bp in blueprints:
    app.register_blueprint(bp, url_prefix=bp.url_prefix)


def play_start_sequence():
    color = (255, 226, 64)
    location_1 = ObjectLocation(1, 15)
    spot_1 = LEDSpot((0, 0, 0,), location_1, 2)
    location_2 = ObjectLocation(-1, 15)
    spot_2 = LEDSpot((0, 0, 0,), location_2, 2)
    get_led_controller().add_symbol(spot_1)
    get_led_controller().add_symbol(spot_2)
    get_led_controller().add_animation(spot_1, 'color', color, 0.5)
    get_led_controller().add_animation(spot_2, 'color', color, 0.5)
    get_led_controller().add_animation(spot_1, 'location', ObjectLocation(0, 15), 3.0)
    get_led_controller().add_animation(spot_2, 'location_r', ObjectLocation(0, 15), 3.0)
    time.sleep(3.0-0.5)
    get_led_controller().add_animation(spot_1, 'color', (0, 0, 0,), 0.5)
    get_led_controller().add_animation(spot_2, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot_1.dead = True
    spot_2.dead = True


def all_leds_off():
    get_led_controller().off()

@app.route('/')
def dashboard():
    settings = map(lambda bp: bp.as_json(), blueprints)
    return render_template('dashboard.html', settings=settings)


@app.route('/start', methods=['POST'])
def start():
    activated = (request.form['activate'] == 'true')
    if activated:
        print "start seq"
        thread.start_new_thread(play_start_sequence, ())
    else:
        print "led off"
        all_leds_off()
    return ('', 204)


# teardown method
def signal_handler(signal, frame):
    teardown_led_controller()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
