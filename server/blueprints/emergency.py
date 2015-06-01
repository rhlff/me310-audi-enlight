from flask import render_template, abort, request
from jinja2 import TemplateNotFound

from led_controller.led_objects import LEDAllPulsing
from server.blueprints import SettingsBlueprint
from server.leds import get_led_controller

emergency = SettingsBlueprint('emergency', __name__,
                              display_name="Emergency",
                              url_prefix='/emergency',
                              template_folder='templates')

emergency_light = None

def toggle_emergency_light(activate):
    global emergency_light
    if activate:
        if emergency_light is None:
            color = (255, 0, 0)
            emergency_light = LEDAllPulsing(color, 0.1)
            print "show emergency"
            get_led_controller().add_symbol(emergency_light)
    else:
        if emergency_light is not None:
            get_led_controller().remove_symbol(emergency_light)
            emergency_light = None

@emergency.route('/activate', methods=['POST'])
def activate():
    activated = (request.form['activate'] == 'true')
    toggle_emergency_light(activated)
    return ('', 204)