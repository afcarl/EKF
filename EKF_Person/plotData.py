import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import Car_Param as P

plt.ion()

class plotData:

    def __init__(self):
        self.n_rows = 2
        self.n_cols = 1

        #figure and axis handles
        self.fig, self.ax = plt.subplots(self.n_rows, self.n_cols, sharex=True)

        #create lists to store history
        self.timeH= [] #time history
        self.x_trueH = []    #reference history
        self.x_estH = []    #position history
        self.y_trueH = []
        self.y_estH = []

        #create a handle for each subplot
        self.handle = []
        self.handle.append((myPlot(self.ax[0], ylabel = 'X Position', title = 'EKF')))
        self.handle.append(myPlot(self.ax[1], xlabel = 't (s)', ylabel = 'Y Position'))

    def updatePlots(self, t, measured, estimated):
        #add to the histories and update each plot

        self.timeH.append(t)
        self.x_trueH.append(measured[4])
        self.x_estH.append(estimated.item(0))
        self.y_trueH.append(measured[5])
        self.y_estH.append(estimated.item(1))

        self.handle[0].updatePlot(self.timeH, [self.x_trueH, self.x_estH])
        self.handle[1].updatePlot(self.timeH, [self.y_trueH, self.y_estH])

class myPlot:

    def __init__(self, ax, xlabel = '', ylabel = '', title = '', legend = None):
        #as is a handle to the axis of the figure
        self.legend = legend
        self.ax = ax
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'b']
        self.linestyles = ['-', '-', '--', '-.', ':']
        self.line = []

        #configure the axis
        self.ax.set_ylabel(ylabel)
        self.ax.set_xlabel(xlabel)
        self.ax.set_title(title)
        self.ax.grid = True

        self.init = True #says initialized

    def updatePlot(self, time, data):

        if self.init ==True:
            for i in range(len(data)):
                #create a line object
                self.line.append(Line2D(time, data[i],
                                        color = self.colors[np.mod(i, len(self.colors)-1)],
                                        ls = self.linestyles[np.mod(i, len(self.linestyles)-1)],
                                        label = self.legend if self.legend!=None else None))
                self.ax.add_line(self.line[i])
                self.init = False
                if self.legend!=None:
                    plt.legend(handles= self.line)
        else: #add new data to the plot
            for i in range(len(self.line)):
                self.line[i].set_xdata(time)
                self.line[i].set_ydata(data[i])

            self.ax.relim()
            self.ax.autoscale()
