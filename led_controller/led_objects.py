import math
from datetime import datetime

from led_controller.led_helper import (
    apply_brightness, project_to_led, limit_color_values, hsv_to_rgb
)


class LEDObject(object):
    def __init__(self, color):
        """
        Keyword arguments:
        color -- the color of the LEDObject
        """
        self.color = color
        self.creation_time = datetime.now()
        self.dead = False

    def pixel_color(self, led_location, t):
        raise NotImplementedError('subclasses of LEDObject must provide a pixel_color() method')

    def animations(self):
        return {
            'color': (self.color, self.animate_color),
        }

    def animate_color(self, start_value, end_value, current_time, duration):
        progress = max(0, min(1, current_time/duration))
        r = (end_value[0]-start_value[0])*progress + start_value[0]
        g = (end_value[1]-start_value[1])*progress + start_value[1]
        b = (end_value[2]-start_value[2])*progress + start_value[2]
        self.color = (r, g, b)


class UnlocatedLEDObject(LEDObject):
    pass


class LocatedLEDObject(LEDObject):
    def __init__(self, color, location):
        """
        Keyword arguments:
        location -- the location of the LEDObject
        """
        super(LocatedLEDObject, self).__init__(color)
        self.location = location

    def animations(self):
        animations = super(LocatedLEDObject, self).animations()
        animations.update({
            'location': (self.location, self.animate_location),
            'location_r': (self.location, self.animate_location_reverse),
        })
        return animations

    def animate_location(self, start_val, end_val, current_time,
                         duration, reverse=False):
        progress = max(0, min(1, current_time/duration))
        angle_diff = (end_val.angle-start_val.angle)%360
        angle_diff = angle_diff-360 if reverse else angle_diff
        angle = angle_diff*progress + start_val.angle
        distance = (end_val.distance-start_val.distance)*progress \
                    + start_val.distance
        self.location.angle = angle
        self.location.distance = distance

    def animate_location_reverse(self, start_val, end_val, current_time,
                                 duration):
        self.animate_location(start_val, end_val, current_time, duration, True)


class LEDAll(UnlocatedLEDObject):
    """
    Turns all LEDs on.

    Customization:
    - color
    """
    def pixel_color(self, led_location, t):
        return self.color


class LEDWave(UnlocatedLEDObject):
    """
    Shows a continuous wave on all LEDs.

    Customization:
    - color
    - speed
    - number of crests
    - height of crests
    - minimal color factor of throughs
    """

    def __init__(self, color, speed, period, amplitude=0.3,
                 vertical_shift=0.7):
        """
        Keyword arguments:
        color -- the color of the wave
        speed -- the speed the wave is moving
                 =0 -> no movement
                 >0 -> movement clockwise
                 <0 -> movement counterclockwise
        period -- the number of overall crests of the wave
        amplitude -- (default 0.3)
        vertical_shift -- vertical shift of the curve (default 0.7)
                          The minmal color factor is vertical_shift-amplitude.
        """
        self.wave_func = self.build_wave_function(period, amplitude, vertical_shift)
        self.speed = speed
        super(LEDWave, self).__init__(color)

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
    """
    Shows a simple circular spot at a given location.

    Customization:
    - color
    - location
    - radius of spot
    - time to appear
    - time to disappear
    """
    def __init__(self, color, location, radius, time_appear=0.0,
                 time_disappear=None):
        """
        Keyword arguments:
        color -- the color of the spot
        location -- the location of the spot
        radius -- the radius of the spot (in meters)
        time_appear -- the time the spot need to appear (in seconds)
        time_disappear -- the time the needs to time_disappear (in seconds)
        """
        if time_disappear is not None:
            assert time_appear > 0.0
        super(LEDSpot, self).__init__(color, location)
        self.radius = radius
        self.time_appear = time_appear
        self.time_disappear = time_disappear

    def animations(self):
        animations = super(LEDSpot, self).animations()
        animations.update({
            'radius': (self.radius, self.animate_radius),
        })
        return animations

    def animate_radius(self, start_value, end_value, current_time, duration):
        progress = max(0, min(1, current_time/duration))
        self.radius = (end_value-start_value)*progress + start_value

    def pixel_color(self, led_location, t):
        time_delta = t - self.creation_time
        time_diff = time_delta.total_seconds()

        ref_time = time_diff
        if self.time_appear > 0.0:
            if self.time_disappear is not None:
                ref_time = self.time_appear
                if time_diff > self.time_appear+self.time_disappear:
                    self.dead = True
            else:
                ref_time = max(self.time_appear, time_diff)
        scale = time_diff/ref_time

        offset_x, offset_y = project_to_led(led_location, self.location)
        distance = math.sqrt(offset_x*offset_x + offset_y*offset_y)

        radius = self.radius*scale
        if distance > radius:
            return None

        brightness_factor = max(0, 1 - distance/radius)
        color = apply_brightness(brightness_factor, *self.color)

        if self.time_disappear is not None:
            brightness_factor = max(0, 1 - (time_diff-self.time_appear)/self.time_disappear)
            color = apply_brightness(brightness_factor, *self.color)

        return limit_color_values(*color)


class LEDAllPulsing(UnlocatedLEDObject):
    """
    Let all LEDs alternate between a maximum and minimum brightness value.

    Customization:
    - color
    - speed of alteration
    """
    def __init__(self, color, speed):
        """
        Keyword arguments:
        color -- the color of the LEDs
        speed -- the speed of the alteration
        """
        super(LEDAllPulsing, self).__init__(color)
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
    """
    Shows waves like water dropping into water.

    Customization:
    - color
    - location
    - speed of waves
    - distance between crests
    - decrease rate of crests
    - end after n waves
    """
    def __init__(self, color, location, speed, period=0.5, decrease=0.025, end_after=None):
        """
        Keyword arguments:
        color -- the color of the waves
        location -- the location of the drops
        speed -- the speed of the waves
        period -- the distance between the crests (default=0.5)
        decrease -- the decrease rate of wave crests (default=0.025)
        end_after -- number of drop to be shown (default=None)
        """
        super(LEDContinuousDrop, self).__init__(color, location)
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


class LEDRainbow(UnlocatedLEDObject):
    def __init__(self, color, speed):
        super(LEDRainbow, self).__init__(color)
        self.speed = speed

    def pixel_color(self, led_location, t):
        time_delta = (t - self.creation_time)
        offset = time_delta.total_seconds()/self.speed*360
        v = ((led_location.angle+offset) % 360)*1.0/360
        color = map(lambda x: x*255, hsv_to_rgb(v, 1.0, 1.0))
        return apply_brightness(1.0, *color)
