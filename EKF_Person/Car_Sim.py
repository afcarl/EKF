import numpy as np
import matplotlib.pyplot as plt
import Car_Param as P
from Car_Animation import Car_Animation as Animation
from Dynamics import Dynamics
from plotData import plotData
from Filter import Filter


dynam = Dynamics()
# data = plotData()
anim = Animation()
filter = Filter()

#THE PLOT WILL SHOW THE  X AND Y POSITION THAT THE PERSON IS AWAY FROM THE CAR
#THE ESTIMATE WILL BE IT'S X AND Y POSITION. THIS Measurement is given in a  RADIUS AND ANGLE (NON-LINEAR relationship)
#SEE https://medium.com/@serrano_223/extended-kalman-filters-for-dummies-4168c68e2117

t = P.t0
while t<P.tf:

    t_nextP = t + P.t_plot
    while t < t_nextP: #move the car and person. We are not controlling either just estimating position of person
        filter.estimate(dynam.outputs())
        dynam.propogateDynamics()
        t += P.t_step

    # data.updatePlots(t, dynam.states(), filter.x_hat)
    anim.draw(dynam.states(), filter.ellipseValues())
    plt.pause(.001)

print('Press key to close')
plt.waitforbuttonpress()
plt.close()
