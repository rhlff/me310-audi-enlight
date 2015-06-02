from flask import render_template, abort, request
import threading
import time

from led_controller.led_world import ObjectLocation
from led_controller.led_objects import LEDSpot
from server.blueprints import SettingsBlueprint
from server.leds import get_led_controller

class ObjectDetection(threading.Thread):
    def __init__(self):
        super(ObjectDetection, self).__init__()
        self.stopped = False

    def run(self):
        while not self.stopped:
            pass

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