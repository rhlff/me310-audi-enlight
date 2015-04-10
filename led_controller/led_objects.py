import abc
import math
from datetime import datetime

from led_controller.led_helper import apply_brightness, project_to_led

class LEDObject:
    __metaclass__ = abc.ABCMeta

    def __init__(self, color, intensity):
        self.color = color
        self.intensity = intensity
        self.creation_time = datetime.now()

    @abc.abstractmethod
    def pixel_color(self, led_location, t):
        pass

class UnlocatedLEDObject(LEDObject):
    pass

class LocatedLEDObject(LEDObject):
    def __init__(self, color, intensity, location):
        super(LocatedLEDObject, self).__init__(color, intensity)
        self.location = location

class LEDAll(UnlocatedLEDObject):
    def pixel_color(self, led_location, t):
        return self.color

class LEDSpot(LocatedLEDObject):
    def __init__(self, color, intensity, location, radius):
        super(LEDSpot, self).__init__(color, intensity, location)
        self.radius = radius

    def pixel_color(self, led_location, t):
        offset_x, offset_y = project_to_led(led_location, self.location)
        distance = math.sqrt(offset_x*offset_x + offset_y*offset_y)

        if distance > self.radius:
            return None

        brightness_factor = 1 - distance/self.radius
        return apply_brightness(brightness_factor, *self.color)
