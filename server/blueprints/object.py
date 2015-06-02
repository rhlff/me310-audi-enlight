from flask import render_template, abort, request
import threading
import time

from led_controller.led_world import ObjectLocation
from led_controller.led_objects import LEDSpot
from server.blueprints import SettingsBlueprint
from server.leds import get_led_controller

import numpy as np
import lidar.lidar as lidarModule
import pickle

class ObjectDetection(threading.Thread):
    def __init__(self):
        super(ObjectDetection, self).__init__()
        self.stopped = False

    def run(self):
        while not self.stopped:
            stepNumber, distance = lidar.getData()
            if abs(minValues[stepNumber] - distance) > 50:
                if stdValues[stepNumber] < 40:
                    print "Detected object at angle %f with a distance of %i" % (stepNumber * 1.8, distance)


    def stop(self):
        self.stopped = True

object_detection = SettingsBlueprint('object-detection', __name__,
                                     display_name="Object Detection",
                                     url_prefix='/object',
                                     template_folder='templates')

Color_Default = (255, 255, 255)
Color_People = (255,  245, 191)
Color_Bike = (255, 235, 127)
Color_Car = (255, 226, 64)
Color_Danger = (255, 80, 80)

detection_thread = None

NUMBER_OF_VALUES = 99
NUMBER_OF_MINIMUM_VALUES_PER_AREA = 10

lidar = lidarModule.Lidar()
# graph = livePlot.LivePlot(NUMBER_OF_VALUES)

values = []
for i in range(NUMBER_OF_VALUES):
    values.append([])

stepNumber, distance = lidar.getData()
while stepNumber <> 0:
    stepNumber, distance = lidar.getData()

print '### Step is at 0 now ###'

lidar.resetDataCount()

values = pickle.load(open("scan5MinimumValues", "rb" ))

print '### MIN ###'
print map(np.min, values)
print '### MAX ###'
print map(np.max, values)
print '### STD ###'
print map(np.std, values)
print '###########'

stdValues = map(np.std, values)
minValues = map(np.min, values)

def toggle_object_detection(activate):
    global detection_thread
    if activate:
        if detection_thread is None:
            detection_thread = ObjectDetection()
            detection_thread.start()
    else:
        if detection_thread is not None:
            detection_thread.stop()
            detection_thread = None

@object_detection.route('/activate', methods=['POST'])
def activate():
    object_detection.activated = (request.form['activate'] == 'true')
    toggle_object_detection(object_detection.activated)
    return ('', 204)