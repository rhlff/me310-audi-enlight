from flask import render_template, abort, request
import thread
import time

from led_controller.led_world import ObjectLocation
from led_controller.led_objects import LEDSpot
from server.blueprints import SettingsBlueprint
from server.leds import get_led_controller


testing_parking = SettingsBlueprint('testing-parking', __name__,
                                  display_name="Parking",
                                  url_prefix='/parking',
                                  template_folder='templates')

def show_ped_1():
    color = (237, 183, 21)
    location = ObjectLocation(15, 20)
    spot = LEDSpot((0, 0, 0,), location, 2)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(-45, 10.0), 10.166)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(10.166-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_ped_2():
    time.sleep(7.666)
    color = (237, 183, 21)
    location = ObjectLocation(45, 10)
    spot = LEDSpot((0, 0, 0,), location, 2.0)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(-90, 5.0), 4.5)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(4.5-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_car_1():
    time.sleep(33.166)
    color = (255, 0, 0)
    location = ObjectLocation(10, 10)
    spot = LEDSpot((0, 0, 0,), location, 2.0)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(-90, 2.0), 6.166)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(6.166)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(-160, 10.0), 2.333)
    time.sleep(2.333-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True


def show_parking():
    thread.start_new_thread(show_ped_1, ())
    thread.start_new_thread(show_ped_2, ())
    thread.start_new_thread(show_car_1, ())

def toggle_parking(activate):
    if activate:
        thread.start_new_thread(show_parking, ())

@testing_parking.route('/activate', methods=['POST'])
def activate():
    testing_parking.activated = (request.form['activate'] == 'true')
    toggle_parking(testing_parking.activated)
    return ('', 204)
