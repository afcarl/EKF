import numpy as np
import control as ctrl
import Car_Param as P

class Filter:

    def __init__(self):
        self.x_hat = np.matrix([[P.xp0],
                                [P.yp0],
                                [P.vp_x],
                                [P.vp_y]]) #this is the estimated Cartesian state
        self.x_hat_polar = np.matrix([[0.0], [0.0]]) #the conversion to polar coordinates
        self.ts = P.t_step

        self.Q = np.matrix(.2 * np.identity(4))
        self.R = np.matrix(.01 * np.identity(2))
        self.Kf = np.matrix(np.zeros((2,4)), dtype = 'float')
        self.P = np.matrix(np.zeros((4,4)), dtype = 'float')

        self.G = np.matrix([[1, 0, P.t_step, 0],
                            [0, 1, 0, P.t_step],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])
        self.ellipse_ang = 0.0
        self.x_length = 0.0
        self.y_length = 0.0

    def estimate(self, z): #z contains xc, yc, rp, thetap
        xc = z[0]
        yc = z[1]
        p = np.matrix([[z[2]], [z[3]]])

        self.x_hat[0] = self.x_hat[0] + self.x_hat[2] * self.ts
        self.x_hat[1] = self.x_hat[1] + self.x_hat[3] * self.ts
        self.x_hat[2] = self.x_hat[2]
        self.x_hat[3] = self.x_hat[3]       #DO I NEED TO ADD NOISE TO THESE? Probably

        self.P = self.G * self.P * self.G.T + self.Q
        # print('P1: ', self.P)

        self.calcEllipse()

        x = self.x_hat.item(0) - xc
        y = self.x_hat.item(1) - yc
        H = np.matrix([[x/np.sqrt(x**2 + y**2), y/np.sqrt(x**2 + y**2), 0, 0],
                        [-y/(x**2 + y**2), x/(x**2 + y**2), 0, 0]], dtype = 'float')
        self.Kf = self.P * H.T * np.linalg.inv(H * self.P * H.T + self.R)

        r = np.sqrt(x**2 + y**2)
        theta = np.arctan(y/x)
        z = np.matrix([[r], [theta]])
        # print('z', z)
        # print('p', p)
        self.x_hat = self.x_hat + self.Kf * (p - z)
        self.P = (np.matrix(np.identity(4)) - self.Kf * H) * self.P
        # print('P2: ', self.P)

    def calcEllipse(self):
        scale = 2.4477
        sigma_xy = self.P[0,1]
        sigma_x2 = self.P[0,0]
        sigma_y2 = self.P[1,1]

        self.ellipse_ang = 0.5 * np.arctan(1/P.aspect_ratio * (2 * sigma_xy)/(sigma_x2 - sigma_y2))
        c = np.matrix([[sigma_x2, sigma_xy], [sigma_xy, sigma_y2]])
        e, _ = np.linalg.eig(c)

        if sigma_x2 > sigma_y2:
            self.x_length = np.sqrt(np.max(e)) * scale
            self.y_length = np.sqrt(np.min(e)) * scale
        else:
            self.y_length = np.sqrt(np.max(e)) * scale
            self.x_length = np.sqrt(np.min(e)) * scale

    def ellipseValues(self):
        return [self.x_length, self.y_length, self.ellipse_ang]
