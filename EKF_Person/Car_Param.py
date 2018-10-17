import numpy as np
import control as ctrl

#Car parameters
xc0 = 0.0 #animation will be a 20 x 20
yc0 = 0.0
vc_y = 0.5 #m/s  this will be constant
vc_x = 0.0 #m/s this will be constant
sc = 1.0 #dimension to draw car as a square

#Person parameters
xp0 = 1.5
yp0 = 9.0
vp_x = 0.1 #m/s this is constant
vp_y = 0.2 #m/s this is constant
rp = 0.25 #radius of person represented as a cylinder

# time parameters
t0 = 0.0
tf = 40.0
t_step = 0.01
t_plot = .1

aspect_ratio = 1.0
