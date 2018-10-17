import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import Car_Param as P
import pylab

class Car_Animation:
    def __init__(self):
        self.flag_init = True
        self.fig, self.ax = plt.subplots()
        self.handle = []

        self.x_hatH = []
        self.y_hatH = []
        self.xH = []
        self.yH = []

        plt.axis([-10, 10, -10.0, 10.0])
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'b']

    def draw(self, state, z_hat):
        xc = state[0]
        yc = state[1]
        x_est = z_hat.item(0)
        y_est = z_hat.item(1)

        self.x_hatH.append(x_est)
        self.y_hatH.append(y_est)
        self.xH.append(xc)
        self.yH.append(yc)

        self.ax.cla()
        self.ax.plot(self.xH, self.yH, 'b')
        self.ax.plot(self.x_hatH, self.y_hatH, 'g')


        # self.drawCar([xc, yc])

        # if self.flag_init == True:
        #     self.drawPerson()
        #     self.flag_init = False

    def drawPerson(self):
        i = 0
        for xy in P.z:
            art = patches.CirclePolygon(xy, radius = P.rp, fc = self.colors[np.mod(i, len(self.colors)-1)], ec = 'black')
            self.ax.add_patch(art)
            i +=1

    def drawCar(self, z):
        xc = z[0]
        yc = z[1]

        xy = (xc, yc)
        s = P.sc

        if self.flag_init == True:
            art = patches.CirclePolygon(xy, radius = P.sc, fc = 'blue', ec = 'black')
            self.handle.append(art)
            #The issue is with the rectangle patch. Not sure what is up with it
            # self.handle.append(patches.Rectangle(xy, s, s, fc = 'green', ec = 'black'))
            self.ax.add_patch(self.handle[0])
        else:
            self.handle[0]._xy = xy
            self.ax.add_patch(self.handle[0])
