import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as patches
import Car_Param as P
import pylab

class Car_Animation:
    def __init__(self):
        self.flag_init = True
        self.fig, self.ax = plt.subplots()
        self.handle = []

        plt.axis([-10, 10, -1.0, 19.0])
        self.ax.set_aspect(aspect = P.aspect_ratio)

    def draw(self, state, ellipse):
        xc = state[0]
        yc = state[1]
        xp = state[4]
        yp = state[5]

        self.drawCar([xc, yc])
        self.drawPerson([xp, yp])
        self.drawEllipse([xp, yp], ellipse) #this draws the uncertainty ellipse

        if self.flag_init == True:
            self.flag_init = False

    def drawPerson(self, z):
        xp = z[0]
        yp = z[1]

        xy = [xp, yp]

        if self.flag_init == True:
            art = patches.CirclePolygon(xy, radius = P.rp, fc = 'red', ec = 'black')
            self.handle.append(art)
            # self.handle.append(patches.Circle(xy, radius = P.rp, fc = 'blue', ec = 'black'))
            self.ax.add_patch(self.handle[1])
        else:
            self.handle[1]._xy = xy
            self.ax.add_patch(self.handle[1])

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

    def drawEllipse(self, z, e):

        if self.flag_init == True:
            art = patches.Ellipse(z, e[0], e[1], angle = e[2] * 180/np.pi)
            self.handle.append(art)
            self.ax.add_patch(self.handle[2])
        else:
            ts = self.ax.transData
            self.handle[2].center = z[0], z[1]
            self.handle[2].width = e[0]
            self.handle[2].height = e[1]
            self.handle[2].angle = e[2] * 180 * np.pi
            # tr = mpl.transforms.Affine2D().rotate_deg_around(z[0], z[1], e[2] * 180/np.pi)
            # t = ts + tr
            # self.handle[2].set_transform(t)
