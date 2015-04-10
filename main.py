from led_controller.led_objects import *
from led_controller.led_world import LEDWorldBuilder, ObjectLocation

import opc
import time
from datetime import datetime

if __name__ == '__main__':
    client = opc.Client('172.16.20.233:7890')
    builder = LEDWorldBuilder()
    builder.add_led_strip(0,   60, -0.5, 0.5, 0.5, 0.5, 100.0/60 * -1 * 0.01)
    builder.add_led_strip(60,  60, -0.5, 0.5, 0.5, 0.5, 100.0/60 *  0 * 0.01)
    builder.add_led_strip(120, 60, -0.5, 0.5, 0.5, 0.5, 100.0/60 *  1 * 0.01)
    # builder.add_led_circle(0,   60, 0.5, 100.0/60 * -1 * 0.01)
    # builder.add_led_circle(60,  60, 0.5, 100.0/60 *  0 * 0.01)
    # builder.add_led_circle(120, 60, 0.5, 100.0/60 *  1 * 0.01)
    world = builder.build()

    # led_all = LEDAll((255, 0, 0), 1)

    color = (150, 0, 0)
    location = ObjectLocation(0, 0.5)
    led_spot = LEDSpot(color, 0, location, 200.0/60 * 0.01 * 5)

    now = datetime.now()
    led_wave = LEDWave(color, 0, 1, 15)

    pixels = world.draw([led_wave], now)

    client.put_pixels(pixels)
    client.put_pixels(pixels)

    # angle_inc = 1
    # while True:
    #     led_spot.location.angle += angle_inc

    #     if led_spot.location.angle > 45 or led_spot.location.angle < -45:
    #         angle_inc *= -1

    #     pixels = world.draw([led_spot], 0)
    #     client.put_pixels(pixels)
    #     time.sleep(0.02)

    while True:
        now = datetime.now()
        pixels = world.draw([led_wave], now)
        client.put_pixels(pixels)
        time.sleep(0.02)

