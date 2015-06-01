import numpy as np
import lidar as lidarModule
import livePlot
import sys

NUMBER_OF_VALUES = 99
NUMBER_OF_MINIMUM_VALUES_PER_AREA = 10

def enoughScans(values, numberOfScans):
    numberOfMissingAreas = len(filter(lambda x: len(x) < numberOfScans, values))

    sys.stdout.write("### Still waiting for %d areas to have enough values \r ###" % ( numberOfMissingAreas ))
    sys.stdout.flush()

    return False if numberOfMissingAreas > 0 else True


lidar = lidarModule.Lidar()
graph = livePlot.LivePlot(NUMBER_OF_VALUES)

values = []
for i in range(NUMBER_OF_VALUES):
    values.append([])

stepNumber, distance = lidar.getData()
while stepNumber <> 0:
    stepNumber, distance = lidar.getData()

print '### Step is a 0 now ###'

lidar.resetDataCount()

while not enoughScans(values, NUMBER_OF_MINIMUM_VALUES_PER_AREA):
    stepNumber, distance = lidar.getData()
    values[stepNumber].append(distance)

    graph.refresh(stepNumber, distance)

print '### MIN ###'
print map(np.min, values)
print '### MAX ###'
print map(np.max, values)
print '### STD ###'
print map(np.std, values)
print '###########'

stdValues = map(np.std, values)
minValues = map(np.min, values)

while True:
    stepNumber, distance = lidar.getData()
    if abs(minValues[stepNumber] - distance) > 50:
        if stdValues[stepNumber] < 40:
            print "Detected object at angle %f" % (stepNumber * 1.8)