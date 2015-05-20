from flask import render_template, abort, request
import thread
import time

from led_controller.led_world import ObjectLocation
from led_controller.led_objects import LEDSpot, LEDAllPulsing
from server.blueprints import SettingsBlueprint
from server.leds import get_led_controller


testing_alarm = SettingsBlueprint('testing-alarm', __name__,
                                  display_name="Alarm",
                                  url_prefix='/alarm',
                                  template_folder='templates')

Color_Default = (255, 255, 255)
Color_People = (255,  245, 191)
Color_Bike = (255, 235, 127)
Color_Car = (255, 226, 64)
Color_Danger = (255, 80, 80)

def show_ped_1():
    time.sleep(5.0)
    color = Color_People #(237, 183, 21)
    location = ObjectLocation(355, 25)
    spot = LEDSpot((0, 0, 0,), location, 2.25)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(90, 2.0), 11.666)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(11.666)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(160, 5.0), 2.333)
    time.sleep(2.333-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_ped_2():
    time.sleep(26.0)
    color = Color_People #(237, 183, 21)
    location = ObjectLocation(-45, 8.0)
    spot = LEDSpot((0, 0, 0,), location, 2.25)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(90, 2.0), 5.5)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(5.5)
    get_led_controller().add_animation(spot, 'location', ObjectLocation(160, 8), 2.0)
    time.sleep(2.0-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_car_1():
    time.sleep(40.666)
    color = Color_Car #(255, 255, 255)
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
    time.sleep(33.0)
    color = Color_Bike #(255, 0, 0)
    location = ObjectLocation(-30, 15)
    spot = LEDSpot((0, 0, 0,), location, 2)
    get_led_controller().add_symbol(spot)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(-90, 2.0), 4.666)
    get_led_controller().add_animation(spot, 'color', color, 0.5)
    time.sleep(4.666)
    get_led_controller().add_animation(spot, 'location_r', ObjectLocation(-160, 10), 1.333-0.5)
    time.sleep(1.333-0.5-0.5)
    get_led_controller().add_animation(spot, 'color', (0, 0, 0,), 0.5)
    time.sleep(0.5)
    spot.dead = True

def show_alarm_1():
    time.sleep(40.5)
    color = Color_Danger # (255, 0, 0)
    led_puls = LEDAllPulsing(color, 0.1)
    get_led_controller().add_symbol(led_puls)
    time.sleep(2.0-0.25)
    get_led_controller().add_animation(led_puls, 'color', (0, 0, 0,), 0.25)
    time.sleep(0.5)
    led_puls.dead = True


def show_alarm():
    thread.start_new_thread(show_ped_1, ())
    thread.start_new_thread(show_ped_2, ())
    thread.start_new_thread(show_bike_1, ())
    thread.start_new_thread(show_car_1, ())
    thread.start_new_thread(show_alarm_1, ())

def toggle_alarm(activate):
    if activate:
        thread.start_new_thread(show_alarm, ())

@testing_alarm.route('/activate', methods=['POST'])
def activate():
    testing_alarm.activated = (request.form['activate'] == 'true')
    toggle_alarm(testing_alarm.activated)
    return ('', 204)
