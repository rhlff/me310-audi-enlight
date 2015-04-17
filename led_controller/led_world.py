import math
from led_controller.led_helper import angle_and_distance_for_point

class LEDWorld(object):
    def __init__(self, led_count, led_locations):
        self.led_count = led_count
        self.led_locations = led_locations

    def draw(self, detected_objects, t):
        # return array of rgb values
        rgb_values = [(0, 0, 0)]*self.led_count
        for location in self.led_locations:
            rgb_values[location.opc_index] = self._rgb_for_led(location, detected_objects, t)
        return rgb_values

    def _rgb_for_led(self, led_location, detected_objects, t):
        colors = [l for l in [led_obj.pixel_color(led_location, t) for led_obj in detected_objects] if l]
        if colors:
            color = reduce( (lambda a, b: (a[0]+b[0], a[1]+b[1], a[2]+b[2],)), colors)
            return (min(color[0], 255), min(color[1], 255), min(color[2], 255), )
        return (0, 0, 0) # default: return black

class LEDWorldBuilder(object):
    def __init__(self):
        self.led_locations = {}

    def build(self):
        # maybe sort locations. think about good structur. prevent duplicates
        # print self.led_locations
        led_count = max(self.led_locations.keys()) + 1
        return LEDWorld(led_count, self.led_locations.values())

    def add_led_strip(self, opc_start_index, led_count, start_x, start_y, end_x, end_y, z):
        spacing_x = (end_x - start_x) * 1.0 / led_count
        spacing_y = (end_y - start_y) * 1.0 / led_count
        for i in xrange(led_count):
            current_x, current_y = start_x+i*spacing_x, start_y+i*spacing_y
            angle, distance = angle_and_distance_for_point(current_x, current_y)
            self.led_locations[opc_start_index+i] = LEDLocation(angle, distance, z, opc_start_index+i)
        return self

    def add_led_circle(self, opc_start_index, led_count, radius, z):
        angle_per_led = 360 / led_count
        for i in xrange(led_count):
            self.led_locations[opc_start_index+i] = LEDLocation(angle_per_led*i, radius, z, opc_start_index+i)
        return self

class ObjectLocation(object):
    def __init__(self, angle, distance):
        self.angle = angle % 360
        self.distance = distance

class LEDLocation(ObjectLocation):
    def __init__(self, angle, distance, z, opc_index):
        super(LEDLocation, self).__init__(angle, distance)
        self.z = z
        self.opc_index = opc_index

    def __str__(self):
        return "\n<LEDLocation %d - angle %f - distance %f - z %f" % (self.opc_index, self.angle, self.distance, self.z)

    def __repr__(self):
        return str(self)

