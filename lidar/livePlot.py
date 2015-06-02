from matplotlib import pyplot as plt
import numpy as np

class LivePlot(object):

    def __init__(self, numberOfValues):
        self.refreshRate = 20
        self.counter = 0

        plt.ion()
        self.ydata = [10] * numberOfValues
        self.ax = plt.subplot(111, polar=True)
        self.line, = self.ax.plot(self.ydata)
        self.line.set_xdata(np.arange(0, 2.95, 0.03))

        plt.ylim([0, 700])

    def refresh(self, x, y):
        self.counter += 1

        self.ydata[x] = y
        self.line.set_ydata(self.ydata)

        if self.counter % self.refreshRate == 0:
            self.counter = 0

            plt.draw()