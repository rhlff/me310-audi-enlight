from flask import render_template, abort, request
import thread
import time

from led_controller.led_world import ObjectLocation
from led_controller.led_objects import LEDSpot
from server.blueprints import SettingsBlueprint
from server.leds import get_led_controller


testing_bike = SettingsBlueprint('testing-bike', __name__,
                                  display_name="Bike",
                                  url_prefix='/bike',
                                  template_folder='templates')

Color_Default = (255, 255, 255)
Color_People = (255,  245, 191)
Color_Bike = (255, 235, 127)
Color_Car = (255, 226, 64)
Color_Danger = (255, 80, 80)

def show_ped_1():
    time.sleep(1.0)
    color = Color_People #(237, 183, 21)
    location = ObjectLocation(-30, 15)
    spot = LEDSpot((0, 0, 0,), location, 2)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(-90, 5), 5.0)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(5.0)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(-190, 15), 5.0)
    time.sleep(5.0-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_car_1():
    time.sleep(15.0)
    color = Color_Car #(255, 0, 0)
    location = ObjectLocation(-30, 25)
    spot = LEDSpot((0, 0, 0,), location, 2)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(-90, 3), 2.0)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(2.0)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(-150, 25), 2.0)
    time.sleep(2.0-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_bike_1():
    time.sleep(17.0)
    color = Color_Bike #(0, 0, 255)
    location = ObjectLocation(5, 25)
    spot = LEDSpot((0, 0, 0,), location, 2)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(90, 3), 8.0)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(8.0)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(135, 10), 3.0)
    time.sleep(3.0)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(90, 2), 3.333)
    time.sleep(3.333)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(0, 10), 4.0)
    time.sleep(4.0-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_bike_2():
    time.sleep(35.5)
    color = Color_Bike #(0, 0, 255)
    location = ObjectLocation(45, 10)
    spot = LEDSpot((0, 0, 0,), location, 2)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(-90, 2), 2.333)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(2.333)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(-170, 25), 10.666)
    time.sleep(10.666-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_ped_2():
    time.sleep(35.5)
    color = Color_People #(237, 183, 21)
    location = ObjectLocation(80, 10)
    spot = LEDSpot((0, 0, 0,), location, 2)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(30, 5), 2.0)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(2.0)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(90, 2), 1.333)
    time.sleep(1.333)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(170, 20), 9.666)
    time.sleep(9.666-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_bike_testing():
    thread.start_new_thread(show_ped_1, ())
    thread.start_new_thread(show_car_1, ())
    thread.start_new_thread(show_bike_1, ())
    thread.start_new_thread(show_bike_2, ())
    thread.start_new_thread(show_ped_2, ())

def toggle_bike(activate):
    if activate:
        thread.start_new_thread(show_bike_testing, ())



@testing_bike.route('/activate', methods=['POST'])
def activate():
    testing_bike.activated = (request.form['activate'] == 'true')
    toggle_bike(testing_bike.activated)
    return ('', 204)
