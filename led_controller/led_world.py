import math
from led_controller.led_helper import (
    angle_and_distance_for_point, limit_color_values
)


class LEDWorld(object):
    """
    This virtual LED system handles the visualization of objects on every LED.
    """
    def __init__(self, led_count, led_locations):
        self.led_count = led_count
        self.led_locations = led_locations

    def draw(self, detected_objs, t):
        # return array of rgb values
        rgb_values = [(0, 0, 0)]*self.led_count
        for l in self.led_locations:
            rgb_values[l.opc_index] = self._rgb_for_led(l, detected_objs, t)
        return rgb_values

    def _rgb_for_led(self, led_location, detected_objs, t):
        colors = [l
                  for l in [led_obj.pixel_color(led_location, t)
                            for led_obj in detected_objs]
                  if l]
        if colors:
            color = reduce((lambda a, b: (a[0]+b[0], a[1]+b[1], a[2]+b[2],)),
                           colors)
            return limit_color_values(*color)
        return (0, 0, 0)  # default: return black


class LEDWorldBuilder(object):
    """
    Builder to create a virtual LED system
    """
    def __init__(self):
        self.led_locations = {}

    def build(self):
        led_count = max(self.led_locations.keys()) + 1
        return LEDWorld(led_count, self.led_locations.values())

    def add_led_strip(self, opc_start_index, led_count, start_x, start_y,
                      end_x, end_y, z, reverse=False):
        """
        Add a line of LEDs from point A to point B to the LED system

        Keyword arguments:
        opc_start_index -- start index for the open pixel control
        led_count -- number of LEDs
        start_x -- x coordinate of point A
        start_y -- y coordinate of point A
        end_x -- x coordinate of point B
        end_y -- y coordinate of point B
        z -- the vertical offset of the LED
        reverse -- revese the opc_index of the LEDs (default=False)
        """
        if reverse:  # switch start and end point
            start_x, start_y, end_x, end_y = end_x, end_y, start_x, start_y
        spacing_x = (end_x - start_x) * 1.0 / (led_count-1)
        spacing_y = (end_y - start_y) * 1.0 / (led_count-1)
        for i in xrange(led_count):
            cur_x, cur_y = start_x+i*spacing_x, start_y+i*spacing_y
            angle, distance = angle_and_distance_for_point(cur_x, cur_y)
            led = LEDLocation(angle, distance, z, opc_start_index+i)
            self.led_locations[opc_start_index+i] = led
        return self

    def add_led_circle(self, opc_start_index, led_count, radius, z,
                       reverse=False):
        """
        Add a circle of LEDs to the LED system

        Keyword arguments:
        opc_start_index -- start index for the open pixel control
        led_count -- number of LEDs
        radius -- the radius of the LED circle
        z -- the vertical offset of the LED
        reverse -- revese the opc_index of the LEDs (default=False)
        """
        angle_per_led = 360 / led_count
        angle_per_led = angle_per_led*-1 if reverse else angle_per_led
        for i in xrange(led_count):
            led = LEDLocation(angle_per_led*i, radius, z, opc_start_index+i)
            self.led_locations[opc_start_index+i] = led
        return self


class ObjectLocation(object):
    """
    Represents a generic object in the virtual space.
    """
    def __init__(self, angle, distance):
        self.angle = angle % 360
        self.distance = distance


class LEDLocation(ObjectLocation):
    """
    Represents a LED in the virtual space.
    """
    def __init__(self, angle, distance, z, opc_index):
        super(LEDLocation, self).__init__(angle, distance)
        self.z = z
        self.opc_index = opc_index

    def __str__(self):
        return "\n<LEDLocation %d - angle %f - distance %f - z %f" % \
            (self.opc_index, self.angle, self.distance, self.z)

    def __repr__(self):
        return str(self)
