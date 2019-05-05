import math
import pgzrun

class Ship:
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.gas = 750
        self.ang = 0
        self.xVel = 0
        self.yVel = 0
        self.accMode = 0
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

    def frange(x, y, jump):
        while x < y:
            yield x
            x += jump

    def getXpos(self):
        return self.xpos

    def getYpos(self):
        return self.ypos

    def setPos(self, x, y):
        self.xpos = x
        self.ypos = y

    def getXvel(self):
        return self.xVel

    def getYvel(self):
        return self.yVel

    def setVel(self, xv, yv):
        self.xVel = xv
        self.yVel = yv

    def getGas(self):
        return self.gas

    def setGas(self, g):
        self.gas = g

    def rotate(self, newAng):
        if newAng > 0:
            self.ang = 0
        elif newAng < -180:
            self.ang = -180
        else:
            self.ang = newAng

    def setAng(self, angle):
        self.ang = angle

    def getAng(self):
        return self.ang

    def setAccMode(self, mode):
        self.accMode = mode

    def getAccMode(self):
        return self.accMode

    def accelerate(self, xv, yv):
        xv = xv + .025*self.accMode*math.cos(math.radians(self.ang))
        yv = yv + .035*self.accMode*math.sin(math.radians(self.ang))
        self.gas = self.gas - .015*self.accMode
        if self.gas < 0:
            self.gas = 0

    def accelerateChange(self, modifier):
        self.accMode = self.accMode + modifier
        if self.accMode < 0 or self.accMode > 8:
            self.accMode = self.accMode - modifier
        if self.gas <= 0:
            self.accMode = 0

    def draw(self, screen):
        screen.draw.line((self.xpos - 6.0*math.cos(math.radians(self.ang) + (math.pi / 6.0)), self.ypos - 6.0*math.sin(math.radians(self.ang) + math.pi / 6.0)),
            (self.xpos - 12.0*math.cos(math.radians(self.ang) + (math.pi / 6.0)), self.ypos - 12.0*math.sin(math.radians(self.ang) + math.pi / 6.0)), (255, 255, 255))
        screen.draw.line((self.xpos - 6.0*math.cos(math.radians(self.ang) - (math.pi / 6.0)), self.ypos - 6.0*math.sin(math.radians(self.ang) - math.pi / 6.0)),
            (self.xpos - 12.0*math.cos(math.radians(self.ang) - (math.pi / 6.0)), self.ypos - 12.0*math.sin(math.radians(self.ang) - math.pi / 6.0)), (255, 255, 255))
        if self.accMode > 0:
            screen.draw.line((self.xpos - 6.0*math.cos(math.radians(self.ang) + (math.pi / 6.0)), self.ypos - 6.0*math.sin(math.radians(self.ang) + math.pi / 6.0)),
                (self.xpos - 6.0*math.cos(math.radians(self.ang)) - (float(self.accMode))*2.0*math.cos(math.radians(self.ang)), self.ypos - 6.0*math.sin(math.radians(self.ang)) -(float(self.accMode))*2.0*math.sin(math.radians(self.ang))), (255, 255, 255))
            screen.draw.line((self.xpos - 6.0*math.cos(math.radians(self.ang) - (math.pi / 6.0)), self.ypos - 6.0*math.sin(math.radians(self.ang) - math.pi / 6.0)),
                (self.xpos - 6.0*math.cos(math.radians(self.ang)) - (float(self.accMode))*2.0*math.cos(math.radians(self.ang)), self.ypos - 6.0*math.sin(math.radians(self.ang)) -(float(self.accMode))*2.0*math.sin(math.radians(self.ang))), (255, 255, 255))
        screen.draw.circle((self.xpos, self.ypos), 6, (255,255,255))

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

        for i in self.frange(0, 2.0*math.pi, 0.25):
            self.bodyXPoints.append(int(round(self.xpos - 6.0*math.cos(i))))
            self.bodyYPoints.append(int(round(self.ypos - 6.0*math.sin(i))))

        for i in self.frange(6.0, 11.0, 1):
            self.leg1XPoints.append(int(round(self.xpos - i*math.cos(math.radians(self.ang) + (math.pi/6.0)))))
            self.leg1YPoints.append(int(round(self.ypos - i*math.sin(math.radians(self.ang) + (math.pi/6.0)))))
            self.leg2XPoints.append(int(round(self.xpos - i*math.cos(math.radians(self.ang) - (math.pi/6.0)))))
            self.leg2YPoints.append(int(round(self.ypos - i*math.sin(math.radians(self.ang) - (math.pi/6.0)))))

        for i in self.frange(11.0, 12.0, 1):
            self.foot1XPoints.append(int(round(self.xpos - i*math.cos(math.radians(self.ang) + (math.pi/6.0)))))
            self.foot1YPoints.append(int(round(self.ypos - i*math.sin(math.radians(self.ang) + (math.pi/6.0)))))
            self.foot2XPoints.append(int(round(self.xpos - i*math.cos(math.radians(self.ang) - (math.pi/6.0)))))
            self.foot2YPoints.append(int(round(self.ypos - i*math.sin(math.radians(self.ang) - (math.pi/6.0)))))
