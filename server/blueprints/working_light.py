from flask import render_template, abort, request
from jinja2 import TemplateNotFound

from led_controller.led_world import ObjectLocation
from led_controller.led_objects import LEDSpot
from server.blueprints import SettingsBlueprint
from server.leds import get_led_controller


working_light = SettingsBlueprint('working-light', __name__,
                                  display_name="Working Light",
                                  url_prefix='/workinglight',
                                  template_folder='templates')
working_light.has_page = True

working_light_led = None


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


@working_light.route('/')
def show():
    try:
        return render_template('working_light.html')
    except TemplateNotFound:
        abort(404)


@working_light.route('/activate', methods=['POST'])
def activate():
    working_light.activated = (request.form['activate'] == 'true')
    toggle_working_light(working_light.activated)
    return ('', 204)
