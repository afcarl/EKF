import numpy as np
import matplotlib.pyplot as plt
import Car_Param as P
from Car_Animation import Car_Animation as Animation
from Dynamics import Dynamics
from Filter import Filter


anim = Animation()
dynam = Dynamics()
filter = Filter()

t = P.t0
while t<P.tf:

    t_nextP = t + P.t_plot
    while t < t_nextP: #move the car and person. We are not controlling either just estimating position of person
        filter.estimate(dynam.outputs(), dynam.control_outputs())
        dynam.propogateDynamics()
        t += P.t_step

    anim.draw(dynam.states(), filter.x_hat)
    plt.pause(.001)

print('Press key to close')
plt.waitforbuttonpress()
plt.close()
