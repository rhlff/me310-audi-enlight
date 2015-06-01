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

working_light_led_front_left = None
working_light_led_front_right = None
working_light_led_back_left = None
working_light_led_back_right = None

def toggle_working_light_front_left(activate):
    global working_light_led_front_left
    if activate:
        if working_light_led_front_left is None:
            color = (237, 183, 21)
            location = ObjectLocation(-45, 90)
            working_light_led_front_left = LEDSpot(color, location, 120)
            print "show working light fl"
            get_led_controller().add_symbol(working_light_led_front_left)
    else:
        if working_light_led_front_left is not None:
            get_led_controller().remove_symbol(working_light_led_front_left)
            working_light_led_front_left = None

def toggle_working_light_front_right(activate):
    global working_light_led_front_right
    if activate:
        if working_light_led_front_right is None:
            color = (237, 183, 21)
            location = ObjectLocation(45, 90)
            working_light_led_front_right = LEDSpot(color, location, 120)
            print "show working light fr"
            get_led_controller().add_symbol(working_light_led_front_right)
    else:
        if working_light_led_front_right is not None:
            get_led_controller().remove_symbol(working_light_led_front_right)
            working_light_led_front_right = None

def toggle_working_light_back_left(activate):
    global working_light_led_back_left
    if activate:
        if working_light_led_back_left is None:
            color = (237, 183, 21)
            location = ObjectLocation(-135, 90)
            working_light_led_back_left = LEDSpot(color, location, 120)
            print "show working light bl"
            get_led_controller().add_symbol(working_light_led_back_left)
    else:
        if working_light_led_back_left is not None:
            get_led_controller().remove_symbol(working_light_led_back_left)
            working_light_led_back_left = None

def toggle_working_light_back_right(activate):
    global working_light_led_back_right
    if activate:
        if working_light_led_back_right is None:
            color = (237, 183, 21)
            location = ObjectLocation(135, 90)
            working_light_led_back_right = LEDSpot(color, location, 120)
            print "show working light br"
            get_led_controller().add_symbol(working_light_led_back_right)
    else:
        if working_light_led_back_right is not None:
            get_led_controller().remove_symbol(working_light_led_back_right)
            working_light_led_back_right = None


@working_light.route('/')
def show():
    try:
        return render_template('working_light.html')
    except TemplateNotFound:
        abort(404)


@working_light.route('/activateFrontLeft', methods=['POST'])
def activate():
    activated = (request.form['activate'] == 'true')
    toggle_working_light_front_left(activated)
    return ('', 204)

@working_light.route('/activateFrontRight', methods=['POST'])
def activateFR():
    activated = (request.form['activate'] == 'true')
    toggle_working_light_front_right(activated)
    return ('', 204)

@working_light.route('/activateBackLeft', methods=['POST'])
def activateBL():
    activated = (request.form['activate'] == 'true')
    toggle_working_light_back_left(activated)
    return ('', 204)

@working_light.route('/activateBackRight', methods=['POST'])
def activateBR():
    activated = (request.form['activate'] == 'true')
    toggle_working_light_back_right(activated)
    return ('', 204)

@working_light.route('/activateAll', methods=['POST'])
def activateAll():
    activated = (request.form['activate'] == 'true')
    toggle_working_light_front_left(activated)
    toggle_working_light_front_right(activated)
    toggle_working_light_back_left(activated)
    toggle_working_light_back_right(activated)
    return ('', 204)
