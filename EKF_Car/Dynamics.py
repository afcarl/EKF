import numpy as np
import Car_Param as P
import math

class Dynamics:
    def __init__(self):
        self.state = np.matrix([[P.xc0],
                                [P.yc0],
                                [P.theta0]]) #this last entry is the velocity

        self.ts = P.t_step
        self.prev_x = P.xc0
        self.prev_y = P.yc0
        self.prev_theta = P.theta0
        self.landmarks = []
        self.v = P.vc
        self.w = P.wc


    def propogateDynamics(self):

        A = np.matrix([[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1]])
        B = np.matrix([[self.ts * np.cos(self.state.item(2)), 0],
                        [self.ts * np.sin(self.state.item(2)), 0],
                        [0, self.ts]])
        u = np.matrix([[self.v], [self.w]])

        self.state = A * self.state + B * u

    def outputs(self):
        xc = self.state.item(0) + np.random.randn() * P.Qsim[0,0]
        yc = self.state.item(1) + np.random.randn() * P.Qsim[1, 1]
        # theta = self.state.item(2) + np.random.randn()

        return [xc, yc]

    def control_outputs(self):
        v = self.v + np.random.randn() * P.Rsim[0,0]
        w = self.w + np.random.randn() * P.Rsim[1,1]

        return [v, w]

    def landmark_outputs(self):
        #this will output the r and theta and s (whatever that is) to every
        #landmark within a certain radius of the car (4m?)
        #vary by .5m and 3 deg
        v_r = .5
        v_theta = 5.0 * np.pi/180.0
        i = 0
        self.landmarks = []

        for [x_l, y_l] in P.z:
            u_r = np.random.normal(0, v_r/3.0, 1)
            u_theta = np.random.normal(0, v_theta/3.0, 1)
            #do i need one for the signature?

            x = x_l - self.state.item(0)
            y = y_l - self.state.item(1)
            r = np.sqrt(x**2 + y**2)
            if r <= P.range:
                phi = math.atan2(y, x) - self.state.item(2) + u_theta.item(0) #this might need to be adjusted slightly
                # print(r)
                r = r + u_r.item(0)
                temp = [i, r, phi] # i is the index of the landmark. Is i the s?
                self.landmarks.append(temp)
            i += 1

        return self.landmarks

    def states(self):
        return self.state.T.tolist()[0]
