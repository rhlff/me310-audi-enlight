import numpy as np
import lidar as lidarModule
import livePlot
import sys

# from random import randint
# step = 1
# valueStepper = 1

# def getFakeData():
#     global step, valueStepper

#     if step == 99 or step == 0:
#         valueStepper *= -1

#     step += valueStepper
#     # value = randint(100, 600)
#     value = 110

#     return "%i %i" % (step, value)

def funcOrZero(x):
    if len(x) >= 3:
        return np.min(x)
    else:
        print 'unusable'
        return 0

def enoughScans(values, numberOfScans):
    sys.stdout.write("### Still waiting for %d areas to have enough values \r ###" % (len(filter(lambda x: len(x) < numberOfScans, values))) )
    sys.stdout.flush()

    if len(filter(lambda x: len(x) < numberOfScans, values)) == 2:
        print filter(lambda x: len(x) < numberOfScans, values)

    return False if len(filter(lambda x: len(x) < numberOfScans, values)) > 0 else True


lidar = lidarModule.Lidar()
graph = livePlot.LivePlot(99)

values = []
for i in range(99):
    values.append([])

stepNumber, distance = lidar.getData()
while stepNumber <> 0:
    stepNumber, distance = lidar.getData()

print '### Step is a 0 now ###'

lidar.resetDataCount()

while not enoughScans(values, 10):
    stepNumber, distance = lidar.getData()
    values[stepNumber].append(distance)

    graph.refresh(stepNumber, distance)

print '### MIN ###'
print map(np.min, values)
print '### MAX ###'
print map(np.max, values)
print '### STD ###'
print map(np.std, values)
stdValues = map(np.std, values)
minValues = map(funcOrZero, values)


while True:
    stepNumber, distance = lidar.getData()
    if abs(minValues[stepNumber] - distance) > 50:
        if stdValues[stepNumber] < 40:
            print "Detected object at angle %f" % (stepNumber * 1.8)