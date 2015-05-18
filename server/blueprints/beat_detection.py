from flask import render_template, abort, request
from jinja2 import TemplateNotFound

from led_controller.led_world import ObjectLocation
from led_controller.led_objects import LEDSpot
from server.blueprints import SettingsBlueprint
from server.leds import get_led_controller


beat_detection = SettingsBlueprint('beat-detection', __name__,
                                   display_name="Beat Detection",
                                   url_prefix='/beatdetection',
                                   template_folder='templates')


@beat_detection.route('/')
def show():
    try:
        return render_template('working_light.html')
    except TemplateNotFound:
        abort(404)


@beat_detection.route('/activate', methods=['POST'])
def activate():
    beat_detection.activated = (request.form['activate'] == 'true')
    return ('', 204)


@beat_detection.route('/beat', methods=['POST'])
def receive_beat():
    energy = float(request.form['energy'])
    if beat_detection.activated:
        if energy > 2.0:
            color = (237, 183, 21)
            location = ObjectLocation(0, 1.5)
            led_spot = LEDSpot(color, location, 1.0/60 * 30, 0.35, 0.75)
            get_led_controller().add_symbol(led_spot)
        elif energy > 1.0:
            color = (191, 75, 17)
            location = ObjectLocation(-45, 1.0)
            led_spot1 = LEDSpot(color, location, 1.0/60 * 15, 0.25, 0.25)
            location = ObjectLocation(45, 1.0)
            led_spot2 = LEDSpot(color, location, 1.0/60 * 15, 0.25, 0.25)
            get_led_controller().add_symbol(led_spot1)
            get_led_controller().add_symbol(led_spot2)

    return ('', 204)
