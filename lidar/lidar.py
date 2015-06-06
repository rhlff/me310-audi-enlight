import time
import serial
from RF24 import *

class Lidar(object):

    def __init__(self):
        self.lastStep = -1
        self.dataCollected = 0
        self.skipNext = False

        self.radio = RF24(RPI_BPLUS_GPIO_J8_15, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)
        pipes = [0xE8E8F0F0E1, 0xF0F0F0F0D2]
        self.radio.begin()
        self.radio.setRetries(15,15)
        self.radio.openReadingPipe(1,pipes[0])
        self.radio.setAutoAck(False)
        self.radio.startListening()

        time.sleep(1.0)
        self.avoidJunkValue()

    def avoidJunkValue(self):
        if self.radio.available():
            receive_payload = self.radio.read2()

    def getData(self):
        data = self.radio.read2().split(' ')
        if self.skipNext:
            self.skipNext = False
            return -1, -1

        while len(data) <> 2 or data[0] == '' or int(data[0]) == self.lastStep or int(data[1]) < 0:
            data = self.radio.read2().split(' ')

        stepNumber = int(data[0])
        distance = int(data[1])

        if distance > 80000:
            self.skipNext = True


        distance = distance if distance <= 650 else 650

        self.lastStep = stepNumber

        self.dataCollected += 1

        return stepNumber, distance

    def resetDataCount(self):
        self.dataCollected = 0
