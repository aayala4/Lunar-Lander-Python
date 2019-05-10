import math

PI = 3.1415926

# Ship class
class Ship:
    # Initialize ship state
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.gas = 750
        self.ang = 0
        self.xVel = 0
        self.yVel = 0

        # Indicates power setting of thruster
        self.accMode = 0

        # Points of collision detection
        self.foot1XPoints = []
        self.foot1YPoints = []
        self.foot2XPoints = []
        self.foot2YPoints = []
        self.leg1XPoints = []
        self.leg1YPoints = []
        self.leg2XPoints = []
        self.leg2YPoints = []
        self.bodyXPoints = []
        self.bodyYPoints = []

    # Range equivalent for floats
    # From: https://stackoverflow.com/questions/7267226/range-for-floats
    def frange(self, x, y, jump):
        while x < y:
            yield x
            x += jump

    # Get x position
    def getXpos(self):
        return self.xpos

    # Get y position
    def getYpos(self):
        return self.ypos

    # Set x and y positions
    def setPos(self, x, y):
        self.xpos = x
        self.ypos = y

    # Get x velocity
    def getXvel(self):
        return self.xVel

    # Get y velocity
    def getYvel(self):
        return self.yVel

    # Set x and y velocities
    def setVel(self, xv, yv):
        self.xVel = xv
        self.yVel = yv

    # Get gas
    def getGas(self):
        return self.gas

    # Set gas
    def setGas(self, g):
        if g < 0:
            self.gas = 0
        else:
            self.gas = g

    # Rotate ship. Min angle of -PI and max angle of 0
    def rotate(self, newAng):
        if newAng > 0:
            self.ang = 0
        elif newAng < -PI:
            self.ang = -PI
        else:
            self.ang = newAng

    # Set angle
    def setAng(self, angle):
        self.ang = angle

    # Get angle
    def getAng(self):
        return self.ang

    # Set thrust power mode
    def setAccMode(self, mode):
        self.accMode = mode

    # Get thrust power mode
    def getAccMode(self):
        return self.accMode

    # Calculate new x and y velocities based on thrust power. Consumes gas.
    def accelerate(self, xv, yv):
        xv = xv + .09*self.accMode*math.cos(self.ang)
        yv = yv + .175*self.accMode*math.sin(self.ang)
        self.gas = self.gas - .08*self.accMode
        if self.gas < 0:
            self.gas = 0
        return xv, yv

    # Change thrust power based on given modifier. Max thrust power of 8 and min of 0.
    def accelerateChange(self, modifier, sounds):
        self.accMode = self.accMode + modifier
        if self.accMode > 0:
            sounds.rocket_thrust.play(-1)
        if self.accMode < 0 or self.accMode > 8:
            self.accMode = self.accMode - modifier
        if self.accMode == 0:
            sounds.rocket_thrust.stop()
        if self.gas <= 0:
            self.accMode = 0

    # Draw ship
    def draw(self, screen):
        screen.draw.line((self.xpos - 6.0*math.cos(self.ang + (PI / 6.0)), self.ypos - 6.0*math.sin(self.ang + PI / 6.0)),
            (self.xpos - 12.0*math.cos(self.ang + (PI / 6.0)), self.ypos - 12.0*math.sin(self.ang + PI / 6.0)), (255, 255, 255))
        screen.draw.line((self.xpos - 6.0*math.cos(self.ang - (PI / 6.0)), self.ypos - 6.0*math.sin(self.ang - PI / 6.0)),
            (self.xpos - 12.0*math.cos(self.ang - (PI / 6.0)), self.ypos - 12.0*math.sin(self.ang - PI / 6.0)), (255, 255, 255))
        if self.accMode > 0:
            screen.draw.line((self.xpos - 6.0*math.cos(self.ang + (PI / 6.0)), self.ypos - 6.0*math.sin(self.ang + PI / 6.0)),
                (self.xpos - 6.0*math.cos(self.ang) - (float(self.accMode))*2.0*math.cos(self.ang), self.ypos - 6.0*math.sin(self.ang) -(float(self.accMode))*2.0*math.sin(self.ang)), (255, 255, 255))
            screen.draw.line((self.xpos - 6.0*math.cos(self.ang - (PI / 6.0)), self.ypos - 6.0*math.sin(self.ang - PI / 6.0)),
                (self.xpos - 6.0*math.cos(self.ang) - (float(self.accMode))*2.0*math.cos(self.ang), self.ypos - 6.0*math.sin(self.ang) -(float(self.accMode))*2.0*math.sin(self.ang)), (255, 255, 255))
        screen.draw.circle((self.xpos, self.ypos), 6, (255,255,255))

    # Check if ship collides with terrain from given terrain vectors
    def collision(self, xt, yt):
        foot1Touch = False
        foot2Touch = False

        for i in range(0, len(xt)):
            for j in range(0, len(self.bodyXPoints)):
                if self.bodyXPoints[j] > xt[i] - 2 and self.bodyXPoints[j] < xt[i] + 2:
                    if self.bodyYPoints[j] > yt[i]:
                        return 1

        for i in range(0, len(xt)):
            for k in range(0, len(self.foot1XPoints)):
                if self.foot1XPoints[k] > xt[i] - 2 and self.foot1XPoints[k] < xt[i] + 2:
                    if self.foot1YPoints[k] >= yt[i]:
                        foot1Touch = True
                if self.foot2XPoints[k] > xt[i] - 2 and self.foot2XPoints[k] < xt[i] + 2:
                    if self.foot2YPoints[k] >= yt[i]:
                        foot2Touch = True
                if foot1Touch and foot2Touch:
                    return 2

        for i in range(0, len(xt)):
            for k in range(0, len(self.leg1XPoints)):
                if self.leg1XPoints[k] > xt[i] - 2 and self.leg1XPoints[k] < xt[i] + 2:
                    if self.leg1YPoints[k] >= yt[i]:
                        return 1
                if self.leg2XPoints[k] > xt[i] - 2 and self.leg2XPoints[k] < xt[i] + 2:
                    if self.leg2YPoints[k] >= yt[i]:
                        return 1

        return 0

    # Calculate and generate hitbox points
    def hitbox(self):
        self.bodyXPoints.clear()
        self.bodyYPoints.clear()
        self.leg1XPoints.clear()
        self.leg1YPoints.clear()
        self.leg2XPoints.clear()
        self.leg2YPoints.clear()
        self.foot1XPoints.clear()
        self.foot1YPoints.clear()
        self.foot2XPoints.clear()
        self.foot2YPoints.clear()

        for i in self.frange(0, 2.0*PI, 0.25):
            self.bodyXPoints.append(int(round(self.xpos - 6.0*math.cos(i))))
            self.bodyYPoints.append(int(round(self.ypos - 6.0*math.sin(i))))

        for i in self.frange(6.0, 11.0, 1):
            self.leg1XPoints.append(int(round(self.xpos - i*math.cos(self.ang + (PI/6.0)))))
            self.leg1YPoints.append(int(round(self.ypos - i*math.sin(self.ang + (PI/6.0)))))
            self.leg2XPoints.append(int(round(self.xpos - i*math.cos(self.ang - (PI/6.0)))))
            self.leg2YPoints.append(int(round(self.ypos - i*math.sin(self.ang - (PI/6.0)))))

        for i in self.frange(11.0, 12.0, 1):
            self.foot1XPoints.append(int(round(self.xpos - i*math.cos(self.ang + (PI/6.0)))))
            self.foot1YPoints.append(int(round(self.ypos - i*math.sin(self.ang + (PI/6.0)))))
            self.foot2XPoints.append(int(round(self.xpos - i*math.cos(self.ang - (PI/6.0)))))
            self.foot2YPoints.append(int(round(self.ypos - i*math.sin(self.ang - (PI/6.0)))))
