import math
from led_controller.led_helper import (
    angle_and_distance_for_point, limit_color_values
)


led_length = 165.0/100/100


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PartConfig(object):
    def __init__(self, point1, point2, point3):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

    def _long_part_first(self):
        length_part_1 = math.sqrt((self.point1.x-self.point2.x)**2
                                  + (self.point1.y-self.point2.y)**2)
        length_part_2 = math.sqrt((self.point2.x-self.point3.x)**2
                                  + (self.point2.y-self.point3.y)**2)
        return length_part_1 > length_part_2

    def length_types(self):
        types = ['short', 'long']
        return reversed(types) if self._long_part_first() else types

    def _subpart_points(self, subpart):
        points = [self.point1, self.point2, self.point3]
        return points[0:2] if subpart == 0 else points[1:3]

    def _center(self, subpart):
        points = self._subpart_points(subpart)
        return Point((points[0].x+points[1].x)/2, (points[0].y+points[1].y)/2)

    def _led_spacing(self, subpart):
        points = self._subpart_points(subpart)
        diff_x = points[0].x - points[1].x
        diff_y = points[0].y - points[1].y
        length = math.sqrt(diff_x**2 + diff_y**2)
        return diff_x/length*led_length, diff_y/length*led_length

    def start_end(self, subpart, led_count):
        center = self._center(subpart)
        led_spacing_x, led_spacing_y = self._led_spacing(subpart)
        return Point(center.x + (led_count-0)*1.0/2*led_spacing_x,
                     center.y + (led_count-0)*1.0/2*led_spacing_y), \
               Point(center.x - (led_count-0)*1.0/2*led_spacing_x,
                     center.y - (led_count-0)*1.0/2*led_spacing_y)


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

    def add_octa_circle(self):
        circle_width = 105.0/100
        part_short_length = 257.2/1000
        part_long_length = 657.2/1000

        led_counts = {
            'short': {
                'inner': 14,
                'middle': 15,
                'outer': 16,
            },
            'long': {
                'inner': 38,
                'middle': 39,
                'outer': 40,
            }
        }

        partConfigs = [
            # # Part A
            # PartConfig(Point(part_long_length/2, circle_width/2 * -1),
            #            Point(circle_width/2, part_long_length/2 * -1),
            #            Point(circle_width/2, part_long_length/2)),
            # # Part B
            # PartConfig(Point(part_long_length/2, circle_width/2 * -1),
            #            Point(part_long_length/2 * -1, circle_width/2 * -1),
            #            Point(circle_width/2 * -1, part_long_length/2 * -1)),
            # Part C
            PartConfig(Point(part_long_length/2 * -1, circle_width/2),
                       Point(circle_width/2 * -1, part_long_length/2),
                       Point(circle_width/2 * -1, part_long_length/2 * -1)),
            # Part D
            PartConfig(Point(part_long_length/2 * -1, circle_width/2),
                       Point(part_long_length/2, circle_width/2),
                       Point(circle_width/2, part_long_length/2)),
        ]

        opc_index = 486 - 162
        for partConfig in partConfigs:
            for offset, row in enumerate(['inner', 'middle', 'outer']): #enumerate(['middle']):
                for subpart, length_type in enumerate(partConfig.length_types()):
                    led_count = led_counts[length_type][row]
                    start, end = partConfig.start_end(subpart, led_count)
                    # print "start:", start.x, start.y, "end:", end.x, end.y
                    self.add_led_strip(opc_index, led_count,
                                          start.x, start.y, end.x, end.y,
                                          (offset-1)*led_length)
                    opc_index += led_count
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
