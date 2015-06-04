from flask import render_template, abort, request
import threading
import time
from datetime import datetime

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
        NUMBER_OF_VALUES = 99
        NUMBER_OF_MINIMUM_VALUES_PER_AREA = 10

        lidar = lidarModule.Lidar()
        # graph = livePlot.LivePlot(NUMBER_OF_VALUES)

        values = []
        spots = []
        for i in range(NUMBER_OF_VALUES):
            values.append([])
            spots.append({'active': False, 'spot': LEDSpot(Color_People, ObjectLocation(i * 1.65, 2), 0.3)})
            # get_led_controller().add_symbol(spots[i])

        # stepNumber, distance = lidar.getData()
        # while stepNumber <> 0:
            # stepNumber, distance = lidar.getData()

        # print '### Step is at 0 now ###'

        lidar.resetDataCount()

        values = pickle.load(open("/Users/max/Documents/code/me310-audi-enlight/lidar/scan6MinimumValues", "rb" ))

        print '### MIN ###'
        print map(np.min, values)
        print '### MAX ###'
        print map(np.max, values)
        print '### STD ###'
        print map(np.std, values)
        print '###########'

        stdValues = map(np.std, values)
        minValues = map(np.min, values)

        spot = None

        # stepNumber, distance = 50, 200
        # location = ObjectLocation(stepNumber * 1.8, distance / 100)
        # spot = LEDSpot(Color_People, location, 2)
        # get_led_controller().add_symbol(spot)

        while not self.stopped:
            stepNumber, distance = lidar.getData()
            # stepNumber, distance = 50, 200
            # time.sleep(0.01)
            if stepNumber == 55:
                continue
            if abs(minValues[stepNumber] - distance) > 50:
                if stdValues[stepNumber] < 40:
                    # spots[stepNumber].color = Color_People
                    if (not spots[stepNumber]['active']):
                        get_led_controller().add_symbol(spots[stepNumber]['spot'])
                        spots[stepNumber]['active'] = True

                        # print datetime.now(), "Detected object at angle %f with a distance of %i" % (stepNumber * 1.8, distance)
            else:
                pass
                get_led_controller().remove_symbol(spots[stepNumber]['spot'])
                # if spots[stepNumber]['active']:
                #     print datetime.now(), "Remove object at angle %f" % (stepNumber*1.8,)
                spots[stepNumber]['active'] = False
                # spots[stepNumber]['spot'].color = Color_None

        for spot in spots:
            get_led_controller().remove_symbol(spot['spot'])


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
Color_None = (0, 0, 0)

detection_thread = None


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