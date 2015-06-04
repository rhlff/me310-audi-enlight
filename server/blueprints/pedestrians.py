from flask import render_template, abort, request
import thread
import time

from led_controller.led_world import ObjectLocation
from led_controller.led_objects import LEDSpot
from server.blueprints import SettingsBlueprint
from server.leds import get_led_controller


pedestrians = SettingsBlueprint('pedestrians', __name__,
                                display_name="Pedestrians",
                                url_prefix='/pedestrians',
                                template_folder='templates')

Color_Default = (255, 255, 255)
Color_People = (255,  245, 191)
Color_Bike = (255, 235, 127)
Color_Car = (255, 226, 64)
Color_Danger = (255, 80, 80)

def show_ped_1():
    color = Color_People #(237, 183, 21)
    location = ObjectLocation(155, 2)
    spot = LEDSpot((0, 0, 0,), location, 0.75)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(0, 2.0), 8.0)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(8.0-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_ped_2():
    time.sleep(1.5)
    color = Color_People #(237, 183, 21)
    location = ObjectLocation(-10, 3.0)
    spot = LEDSpot((0, 0, 0,), location, 0.75)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(180, 2.0), 9.0)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(9.0-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_pedestrians():
    thread.start_new_thread(show_ped_1, ())
    thread.start_new_thread(show_ped_2, ())

def toggle_pedestrians(activate):
    if activate:
        thread.start_new_thread(show_pedestrians, ())

@pedestrians.route('/activate', methods=['POST'])
def activate():
    pedestrians.activated = (request.form['activate'] == 'true')
    toggle_pedestrians(pedestrians.activated)
    return ('', 204)
