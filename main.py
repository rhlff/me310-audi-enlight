from led_controller.led_objects import *
from led_controller.led_world import LEDWorldBuilder, ObjectLocation

import opc, time

if __name__ == '__main__':
    client = opc.Client('172.16.20.233:7890')
    builder = LEDWorldBuilder()
    builder.add_led_strip(0,   60, -0.5, 0.5, 0.5, 0.5, 100.0/60 * -1 * 0.01)
    builder.add_led_strip(60,  60, -0.5, 0.5, 0.5, 0.5, 100.0/60 *  0 * 0.01)
    builder.add_led_strip(120, 60, -0.5, 0.5, 0.5, 0.5, 100.0/60 *  1 * 0.01)
    #builder.add_led_circle(0, 60, 1, 0)
    world = builder.build()

    # led_all = LEDAll((255, 0, 0), 1)
    color = (150, 0, 0)
    location = ObjectLocation(0, 0.5)
    led_all = LEDSpot(color, 0, location, 200.0/60 * 0.01 * 5)
    pixels = world.draw([led_all], 0)

    client.put_pixels(pixels)
    client.put_pixels(pixels)

    angle_inc = 1
    while True:
        led_all.location.angle += angle_inc

        if led_all.location.angle > 45 or led_all.location.angle < -45:
            angle_inc *= -1

        pixels = world.draw([led_all], 0)
        client.put_pixels(pixels)
        time.sleep(0.02)

