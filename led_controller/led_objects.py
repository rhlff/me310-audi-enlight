import abc
from datetime import datetime

class LEDObject:
    __metaclass__ = abc.ABCMeta

    def __init__(self, color, intensity):
        self.color = color
        self.intensity = intensity
        self.creation_time = datetime.now()

    @abc.abstractmethod
    def pixel_color(self, led_location, time):
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

