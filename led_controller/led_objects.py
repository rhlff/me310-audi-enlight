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

class LEDWave(UnlocatedLEDObject):
    def __init__(self, color, intensity, speed, period, amplitude=0.3, vertical_shift=0.7):
        self.wave_function = self.build_wave_function(period, amplitude, vertical_shift)
        self.speed = speed
        super(LEDWave, self).__init__(color, intensity)

    def build_wave_function(self, period, amplitude, vertical_shift):
        def wave_function(angle, phase_shift):
            return amplitude * math.cos(period*(math.radians(angle)-phase_shift*math.pi/period)) + vertical_shift
        return wave_function

    def pixel_color(self, led_location, t):
        time_delta = t - self.creation_time
        time_diff = 0 if self.speed == 0 else time_delta.total_seconds() / self.speed
        brightness_factor = self.wave_function(led_location.angle, time_diff)
        return apply_brightness(brightness_factor, *self.color)

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
