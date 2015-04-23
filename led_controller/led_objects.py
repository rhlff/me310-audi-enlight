import abc
import math
from datetime import datetime

from led_controller.led_helper import (
    apply_brightness, project_to_led, limit_color_values
)


class LEDObject:
    __metaclass__ = abc.ABCMeta

    def __init__(self, color, intensity):
        self.color = color
        self.intensity = intensity
        self.creation_time = datetime.now()
        self.dead = False

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
    def __init__(self, color, intensity, speed, period,
                 amplitude=0.3, vertical_shift=0.7):
        self.wave_func = self.build_wave_function(period, amplitude, vertical_shift)
        self.speed = speed
        super(LEDWave, self).__init__(color, intensity)

    def build_wave_function(self, period, amplitude, vertical_shift):
        def wave_function(angle, phase_shift):
            return amplitude * math.cos(period*(math.radians(angle)-phase_shift*math.pi/period)) + vertical_shift
        return wave_function

    def pixel_color(self, led_location, t):
        time_delta = t - self.creation_time
        time_diff = 0 if self.speed == 0 else time_delta.total_seconds()/self.speed
        brightness_factor = self.wave_func(led_location.angle, time_diff)
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
        color = apply_brightness(brightness_factor, *self.color)
        return limit_color_values(*color)


class LEDDrop(LocatedLEDObject):
    def __init__(self, color, intensity, location, initial_radius, speed):
        super(LEDDrop, self).__init__(color, intensity, location)
        self.initial_radius = initial_radius
        self.speed = speed

    def pixel_color(self, led_location, t):
        offset_x, offset_y = project_to_led(led_location, self.location)
        distance = math.sqrt(offset_x*offset_x + offset_y*offset_y)

        time_delta = t - self.creation_time
        time_diff = 0 if self.speed == 0 else time_delta.total_seconds() / self.speed

        inner_spacing = self.initial_radius * time_diff / 10

        if distance > self.initial_radius + inner_spacing:
            return None

        brightness_factor_time = 1/max(1.0, time_diff/5)
        brightness_factor = min(1, 1 - (distance - inner_spacing)/(self.initial_radius))
        brightness_factor *= brightness_factor_time
        if distance < inner_spacing:
            brightness_factor -= 1 - distance/inner_spacing
        if brightness_factor_time < 0.2:
            self.dead = True
        color = apply_brightness(brightness_factor, *self.color)
        return limit_color_values(*color)


class LEDAllPulsing(UnlocatedLEDObject):
    def __init__(self, color, intensity, speed):
        super(LEDAllPulsing, self).__init__(color, intensity)
        self.speed = speed

    def pixel_color(self, led_location, t):
        heigth = 0.3
        amplitude = heigth/2
        vertical_shift = 1-amplitude

        time_delta = t - self.creation_time
        time_diff = 0 if self.speed == 0 else time_delta.total_seconds() / self.speed

        brightness_factor = amplitude*math.sin(time_diff)+vertical_shift
        return apply_brightness(brightness_factor, *self.color)


class LEDContinuousDrop(LocatedLEDObject):
    def __init__(self, color, intensity, location, interval, speed, period=0.5, decrease=0.025, end_after=None):
        super(LEDContinuousDrop, self).__init__(color, intensity, location)
        self.interval = interval
        self.speed = speed
        self.period = period
        self.decrease = decrease
        self.end_after = end_after

    def pixel_color(self, led_location, t):
        offset_x, offset_y = project_to_led(led_location, self.location)
        distance = math.sqrt(offset_x*offset_x + offset_y*offset_y)
        distance *= 100

        time_delta = t - self.creation_time
        time_diff = 0 if self.speed == 0 else time_delta.total_seconds() / self.speed * 2

        decrease_factor = max(0, 1-self.decrease*distance)
        if self.period*distance/math.pi > time_diff+0.5:
            return None
        if self.end_after:
            if self.period*distance/math.pi < time_diff-self.end_after*2+0.5:
                return None

        brightness_factor = 0.5*(math.cos(self.period*distance+(-1.0*time_diff-1.5)*math.pi)*decrease_factor+decrease_factor)
        return apply_brightness(brightness_factor*1.5, *self.color)
