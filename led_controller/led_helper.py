import math

def apply_brightness(brightness, r, g, b):
    return (brightness*r, brightness*g, brightness*b)

def project_to_led(led_location, symbol_location, scale_factor=1):
    pixel_angle = led_location.angle - symbol_location.angle
    offset_x = pixel_angle * math.pi / 180 * symbol_location.distance
    offset_y = led_location.z * symbol_location.distance / led_location.distance
    return offset_x*scale_factor, offset_y*scale_factor
