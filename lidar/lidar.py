import time
import serial

class Lidar(object):

    def __init__(self):
        self.lastStep = -1
        self.dataCollected = 0

        self.connection = serial.Serial('/dev/tty.usbmodem1411', 119200)
        time.sleep(2.0)
        self.avoidJunkValue()

    def avoidJunkValue(self):
        self.connection.readline()

    def getData(self):
        data = self.connection.readline().split(' ')

        while len(data) <> 2 or data[0] == '' or int(data[0]) == self.lastStep or int(data[1]) < 0:
            data = self.connection.readline().split(' ')

        stepNumber = int(data[0])
        distance = int(data[1])

        distance = distance if distance <= 650 else 650

        self.lastStep = stepNumber

        self.dataCollected += 1

        return stepNumber, distance

    def resetDataCount(self):
        self.dataCollected = 0