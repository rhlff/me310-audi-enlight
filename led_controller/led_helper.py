import math

def apply_brightness(brightness, r, g, b):
    return (brightness*r, brightness*g, brightness*b)

def project_to_led(led_location, symbol_location, scale_factor=1):
    pixel_angle = led_location.angle - symbol_location.angle
    pixel_angle = pixel_angle - 360 if pixel_angle > 180 else pixel_angle
    x = math.radians(pixel_angle) * symbol_location.distance
    y = led_location.z * symbol_location.distance / led_location.distance
    return x*scale_factor, y*scale_factor

def angle_and_distance_for_point(x, y):
    distance = math.sqrt(x*x + y*y)
    angle = math.copysign(math.degrees( math.acos(y / distance) ), x)
    return angle, distance
