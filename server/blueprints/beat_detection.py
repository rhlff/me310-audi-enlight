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
    brightness = 0.5
    if beat_detection.activated:
        if energy > 2.0:
            color = map(lambda x: brightness*x, (237, 183, 21))
            distance = 1.5
            size = 1.0/60 * 30
            appear = 0.25
            disappear = 0.25
            angles = [0, 180]
            for angle in angles:
                location = ObjectLocation(angle, distance)
                led_spot = LEDSpot(color, location, size, appear, disappear)
                get_led_controller().add_symbol(led_spot)
        elif energy > 1.0:
            color = map(lambda x: brightness*x, (191, 115, 77))
            distance = 1.0
            size = 1.0/60 * 15
            appear = 0.25
            disappear = 0.25
            angles = [-35, 35, 145, -145]
            for angle in angles:
                location = ObjectLocation(angle, distance)
                led_spot = LEDSpot(color, location, size, appear, disappear)
                get_led_controller().add_symbol(led_spot)
        elif energy > 0.35:
            color = map(lambda x: brightness*x, (214, 149, 49))
            distance = 1.0
            size = 1.0/60 * 7.5
            appear = 0.25
            disappear = 0.25
            angles = [-70, 70, 110, -110]
            for angle in angles:
                location = ObjectLocation(angle, distance)
                led_spot = LEDSpot(color, location, size, appear, disappear)
                get_led_controller().add_symbol(led_spot)
    return ('', 204)
