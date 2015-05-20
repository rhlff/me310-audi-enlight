from flask import render_template, abort, request
import thread
import time

from led_controller.led_world import ObjectLocation
from led_controller.led_objects import LEDSpot
from server.blueprints import SettingsBlueprint
from server.leds import get_led_controller


testing_alarm = SettingsBlueprint('testing-alarm', __name__,
                                  display_name="Alarm",
                                  url_prefix='/alarm',
                                  template_folder='templates')

def show_ped_1():
    color = (237, 183, 21)
    location = ObjectLocation(355, 25)
    spot = LEDSpot((0, 0, 0,), location, 4)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(90, 2.0), 14.666)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(14.666)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(160, 5.0), 2.333)
    time.sleep(2.333-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_ped_2():
    time.sleep(25.0)
    color = (237, 183, 21)
    location = ObjectLocation(-90, 8.0)
    spot = LEDSpot((0, 0, 0,), location, 3)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(90, 2.0), 6.0)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(6.0)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(160, 8), 2.0)
    time.sleep(2.0-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_car_1():
    time.sleep(40.666)
    color = (255, 0, 0)
    location = ObjectLocation(-45, 3)
    spot = LEDSpot((0, 0, 0,), location, 2)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(0, 3.0), 3.333)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(3.333-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_bike_1():
    time.sleep(32.0)
    color = (255, 0, 0)
    location = ObjectLocation(-5, 15)
    spot = LEDSpot((0, 0, 0,), location, 2)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(-90, 2.0), 4.666)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(6.166)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(-160, 10), 1.333)
    time.sleep(1.333-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True


def show_alarm():
    thread.start_new_thread(show_ped_1, ())
    thread.start_new_thread(show_ped_2, ())
    thread.start_new_thread(show_bike_1, ())
    thread.start_new_thread(show_car_1, ())

def toggle_alarm(activate):
    if activate:
        thread.start_new_thread(show_alarm, ())

@testing_alarm.route('/activate', methods=['POST'])
def activate():
    testing_alarm.activated = (request.form['activate'] == 'true')
    toggle_alarm(testing_alarm.activated)
    return ('', 204)
