import math


def apply_brightness(brightness, r, g, b):
    """
    Adjust brightness of a color.
    """
    return (brightness*r, brightness*g, brightness*b)


def limit_color_values(r, g, b):
    """
    Limits the color values in range 0 to 255.
    """
    return (max(0, min(255, r)),
            max(0, min(255, g)),
            max(0, min(255, b)))


def project_to_led(led_location, symbol_location, scale_factor=1):
    """
    Calculate the x and y coordinate of the symbol visualozation for a given
    led. A scale factor (default 1) is also applied.
    """
    pixel_angle = (led_location.angle - symbol_location.angle) % 360
    pixel_angle = pixel_angle - 360 if pixel_angle > 180 else pixel_angle
    x = math.radians(pixel_angle) * symbol_location.distance
    y = led_location.z * symbol_location.distance / led_location.distance
    return x*scale_factor, y*scale_factor


def angle_and_distance_for_point(x, y):
    """
    Calculate the angle and distance to the origion for a point 2D coordinate
    system.
    """
    distance = math.sqrt(x*x + y*y)
    angle = math.copysign(math.degrees(math.acos(y/distance)), x)
    return angle, distance
