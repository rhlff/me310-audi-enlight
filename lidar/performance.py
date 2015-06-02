import lidar as lidarModule
import time

MEASUREMENTS_TO_TAKE = 1000

lidar = lidarModule.Lidar()

numberOfMeasurements = 0

print "Start measurement now"
before = time.time()

while numberOfMeasurements < MEASUREMENTS_TO_TAKE:
    stepNumber, distance = lidar.getData()
    numberOfMeasurements += 1

after = time.time()
timeDifference = after - before

print "Took %i measurements in %f seconds" % (numberOfMeasurements, timeDifference)