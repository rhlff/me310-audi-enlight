import lidar as lidarModule
import helper as h
import livePlot
import numpy as np
import pickle

NUMBER_OF_VALUES = 99
NUMBER_OF_MINIMUM_VALUES_PER_AREA = 6

lidar = lidarModule.Lidar()
graph = livePlot.LivePlot(NUMBER_OF_VALUES)

stepNumber, distance = lidar.getData()
while stepNumber <> 0:
    stepNumber, distance = lidar.getData()

print '### Step is a 0 now ###'

values = []
for i in range(NUMBER_OF_VALUES):
    values.append([])

while not h.enoughScans(values, NUMBER_OF_MINIMUM_VALUES_PER_AREA):
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

print len(filter(lambda x: x > 40, map(np.std, values)))

pickle.dump(values, open("scan%iMinimumValues" % (NUMBER_OF_MINIMUM_VALUES_PER_AREA), "wb" ))