from flask import render_template, abort, request
from jinja2 import TemplateNotFound

from led_controller.led_world import ObjectLocation
from led_controller.led_objects import LEDContinuousDrop
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
    if beat_detection.activated and float(request.form['energy']) > 1.5:
        location = ObjectLocation(0, 0.5)
        color = (52, 141, 151)
        led_drop = LEDContinuousDrop(color, location, 0.75, period=0.1,
                                     end_after=1)
        get_led_controller().add_symbol(led_drop)
    return ('', 204)
