import numpy as np
import Car_Param as P

class Dynamics:
    def __init__(self):
        #Add uncertainty to the velocities here
        variance = .2
        uncertainty = np.random.normal(0, variance/3.0, 4)
        self.state = np.matrix([[P.xc0],
                                [P.yc0],
                                [P.vc_x * (1 + uncertainty[0])],
                                [P.vc_y * (1 + uncertainty[1])], #end of the cars state
                                [P.xp0],
                                [P.yp0],
                                [P.vp_x * (1 + uncertainty[2])],
                                [P.vp_y * (1 + uncertainty[3])]]) #end of the persons state


    def propogateDynamics(self): #RK4 is not necessary since the velocity is constant otherwise use RK4
        xdot = np.matrix([[P.vc_x],
                        [P.vc_y],
                        [0.0],
                        [0.0],
                        [P.vp_x],
                        [P.vp_y],
                        [0.0],
                        [0.0]])
        self.state = self.state + P.t_step * xdot

    def outputs(self): #this comes from the sensors. Should give the car's position and the radius and angle of the person
        xc = self.state.item(0)
        yc = self.state.item(1)
        xp = self.state.item(4)
        yp = self.state.item(5)

        #ADD NOISE TO THESE VALUES
        # v1 = .5
        # uncertainty = np.random.normal(0, v1/3.0, 2)
        # r = np.sqrt(((xp + uncertainty[0]) - xc)**2 + ((yp+uncertainty[1]) - yc)**2)
        # theta = np.arctan((yp-yc)/(xp-xc))

        v1 = .707
        uncertainty = np.random.normal(0, v1/3.0, 1)
        r = np.sqrt((xp - xc)**2 + (yp - yc)**2) + uncertainty.item(0)
        v2 = .05
        uncertainty = np.random.normal(0, v2/3.0, 1)
        theta = np.arctan((yp-yc)/(xp-xc)) + uncertainty.item(0) #check for case when xp-xc = 0

        return [xc, yc, r, theta]

    def states(self):
        return self.state.T.tolist()[0]
