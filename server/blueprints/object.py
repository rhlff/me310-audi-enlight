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

# The out-commented code is for a more dynamic distance model. The currently used one is based on hard-coded EXPE values

class ObjectDetection(threading.Thread):
    def __init__(self):
        super(ObjectDetection, self).__init__()
        self.stopped = False

    def run(self):
        NUMBER_OF_VALUES = 99
        NUMBER_OF_MINIMUM_VALUES_PER_AREA = 10

        lidar = lidarModule.Lidar()

        # values = []
        spots = []
        for i in range(NUMBER_OF_VALUES):
            # values.append([])
            spots.append({'active': False, 'spot': LEDSpot(Color_Bike, ObjectLocation(i * 1.8 - 10.0, 2), 0.3)})

        # stepNumber, distance = lidar.getData()
        # while stepNumber <> 0:
            # stepNumber, distance = lidar.getData()

        # print '### Step is at 0 now ###'

        minStepDist = [290,290,290,290,290,290,290,290,291,291,292,294,295,297,300,271,241,217,197,180,166,154,144,135,128,121,115,109,104,100,96,92,89,86,83,81,79,77,75,73,71,70,69,67,66,65,64,64,63,62,62,61,61,61,60,60,60,60,60,60,60,61,61,61,62,62,63,64,64,65,66,67,69,70,71,73,75,77,79,81,83,86,89,92,96,100,104,109,115,121,128,135,144,154,166,180,224,224,224]
        maxStepDist = [450,450,470,500,600,600,610,620,610,610,600,590,590,570,560,560,560,560,560,560,560,560,550,540,540,540,540,540,550,550,570,560,560,560,550,550,550,540,550,540,550,560,540,530,530,530,520,500,490,500,510,500,490,490,500,500,500,500,490,480,480,480,470,470,460,460,430,420,420,400,400,400,400,390,390,390,390,390,390,400,410,420,430,450,440,440,440,450,460,470,510,520,520,530,530,530,530,530,530]


        lidar.resetDataCount()

        # values = pickle.load(open("/home/pi/me310-audi-enlight/lidar/scan6MinimumValues", "rb" ))

        # print '### MIN ###'
        # print map(np.min, values)
        # print '### MAX ###'
        # print map(np.max, values)
        # print '### STD ###'
        # print map(np.std, values)
        # print '###########'

        # stdValues = map(np.std, values)
        # minValues = map(np.min, values)

        while not self.stopped:
            stepNumber, distance = lidar.getData()
            if stepNumber == -1:
                continue

            if distance >= maxStepDist[stepNumber] or distance <= minStepDist[stepNumber]:
                if (spots[stepNumber]['active']):
                    get_led_controller().remove_symbol(spots[stepNumber]['spot'])
                    spots[stepNumber]['active'] = False
            else:

                if maxStepDist[stepNumber] - distance > 50:
                        if (not spots[stepNumber]['active']):
                            get_led_controller().add_symbol(spots[stepNumber]['spot'])
                            spots[stepNumber]['active'] = True
                else:
                    if (spots[stepNumber]['active']):
                        get_led_controller().remove_symbol(spots[stepNumber]['spot'])
                        spots[stepNumber]['active'] = False

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