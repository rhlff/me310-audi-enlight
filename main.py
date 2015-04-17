from led_controller.led_objects import *
from led_controller.led_world import LEDWorldBuilder, ObjectLocation

import opc
import time
from datetime import datetime
import argparse

FC_SERVER = '172.16.20.233:7890'
# FC_SERVER = '192.168.2.1:7890'
client = opc.Client(FC_SERVER)

def all_leds_on():
    builder = LEDWorldBuilder().add_led_circle(0, 180, 1, 0)
    world = builder.build()
    led_all = LEDAll((255, 0, 0), 1)
    pixels = world.draw([led_all], None)
    client.put_pixels(pixels)
    client.put_pixels(pixels)

def all_leds_off():
    builder = LEDWorldBuilder().add_led_circle(0, 180, 1, 0)
    world = builder.build()
    led_all = LEDAll((0, 0, 0), 1)
    pixels = world.draw([led_all], None)
    client.put_pixels(pixels)
    client.put_pixels(pixels)

def show_spot():
    builder = LEDWorldBuilder()
    builder.add_led_strip(0,   60, -0.5, 0.5, 0.5, 0.5, 1.0/60 * -1)
    builder.add_led_strip(60,  60, -0.5, 0.5, 0.5, 0.5, 1.0/60 *  0)
    builder.add_led_strip(120, 60, -0.5, 0.5, 0.5, 0.5, 1.0/60 *  1)
    world = builder.build()
    color = (255, 0, 0)
    location = ObjectLocation(0, 1.414213562)
    led_spot = LEDSpot(color, 0, location, 1.0/60 * 20)

    angle_inc = 1
    while True:
        led_spot.location.angle += angle_inc
        if led_spot.location.angle > 45 or led_spot.location.angle < -45:
            angle_inc *= -1
        pixels = world.draw([led_spot], 0)
        client.put_pixels(pixels)
        time.sleep(0.02)

def show_wave():
    builder = LEDWorldBuilder()
    builder.add_led_circle(0,   60, 0.5, 1.0/60 * -1)
    builder.add_led_circle(60,  60, 0.5, 1.0/60 *  0)
    builder.add_led_circle(120, 60, 0.5, 1.0/60 *  1)
    world = builder.build()
    color = (150, 0, 0)
    led_wave = LEDWave(color, 0, 1, 15)

    while True:
        now = datetime.now()
        pixels = world.draw([led_wave], now)
        client.put_pixels(pixels)
        time.sleep(0.02)

def show_drop():
    builder = LEDWorldBuilder()
    builder.add_led_strip(0,   60, -0.5, 0.5, 0.5, 0.5, 1.0/60 * -1)
    builder.add_led_strip(60,  60, -0.5, 0.5, 0.5, 0.5, 1.0/60 *  0)
    builder.add_led_strip(120, 60, -0.5, 0.5, 0.5, 0.5, 1.0/60 *  1)
    world = builder.build()
    location = ObjectLocation(0, 0.5)
    color = (52, 141, 151)
    led_drop = LEDDrop(color, 0, location, 1.0/60 * 10, 0.05)
    symbols = [led_drop]
    while symbols:
        now = datetime.now()
        pixels = world.draw(symbols, now)
        client.put_pixels(pixels)
        symbols = [s for s in symbols if not s.dead]
        time.sleep(0.02)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Interior LED art for ME310 Audi')
    parser.add_argument('pattern', choices=['off', 'all', 'spot', 'wave', 'drop'])
    args = parser.parse_args()

    {
        'all': all_leds_on,
        'off': all_leds_off,
        'spot': show_spot,
        'wave': show_wave,
        'drop': show_drop,
    }[args.pattern]()
