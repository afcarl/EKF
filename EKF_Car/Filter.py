import numpy as np
import control as ctrl
import Car_Param as P
import math

class Filter:

    def __init__(self):
        self.x_hat = np.matrix([[P.xc0],
                                [P.yc0],
                                [P.theta0]]) #Last is initial velocity. this is the estimated state of the car. Some error in initial pose
        self.ts = P.t_step

        self.Q = np.diag([.1, .1, math.radians(1.0)])**2 #Rt in outline. Not sure this is right still
        self.R = np.diag([1.0, math.radians(40.0)])**2   #Qt in outline.
        self.P = np.eye(3)



    def estimate(self, z, u):
        #z contains xc, yc and thetac. u contains v and w
        #l contains in index in P.z, r and theta (from orientation of the car) for each landmark
        #X_HAT DOES NOT CONVERGE
        xc = z[0]
        yc = z[1]
        # theta = z[2]

        v = u[0]
        w = u[1]

        A = np.matrix([[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1]])
        B = np.matrix([[self.ts * np.cos(self.x_hat.item(2)), 0],
                        [self.ts * np.sin(self.x_hat.item(2)), 0],
                        [0, self.ts]])

        self.x_hat = A * self.x_hat + B * np.matrix(u).T

        #Find the Jacobian
        G = np.matrix([[1.0, 0.0, -v * self.ts * np.sin(self.x_hat.item(2))],
                        [0.0, 1.0, v * self.ts * np.cos(self.x_hat.item(2))],
                        [0.0, 0.0, 1.0]])

        self.P = G * self.P * G.T + self.Q

        H = np.matrix([[1.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0]])
        Kf = self.P * H.T * np.linalg.inv(H * self.P * H.T + self.R)

        self.x_hat = self.x_hat + Kf * (np.matrix(z).T - H * self.x_hat)
        self.P = (np.eye(3) - Kf * H) * self.P
