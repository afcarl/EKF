import numpy as np
import control as ctrl
import math

#Car parameters
xc0 = 0.0 #animation will be a 20 x 20
yc0 = 0.0
theta0 = 0.0 # facing right
vc = 1.0 #m/s  this will be constant
wc = 0.1 #rad/s initial angular velocity
sc = .2 #dimension to draw car as a square

#Person parameters
xp0 = 1.5
yp0 = 9.0
z0 = [xp0, yp0]
xp1 = -4.0
yp1 = -4.0
z1 = [xp1, yp1]
xp2 = 5.0
yp2 = -8.0
z2 = [xp2, yp2]
rp = 0.1 #radius of person represented as a cylinder

z = [z0, z1, z2]

range = 20.0

#Simulation noise
Rsim = np.diag([1.0, math.radians(30)])**2
Qsim = np.diag([.5, .5])**2

# time parameters
t0 = 0.0
tf = 40.0
t_step = 0.01
t_plot = .1
