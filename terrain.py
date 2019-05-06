import random

class Terrain:
    def __init__(self):
        self._x = []
        self._y = []

        self._xm = []
        self._ym = []

        self._xp = []
        self._yp = []

        self._multipliersValues = []
        self._multipliersLengths = []
        self._multipliersIndexes = []

        self._xPoints = []

        self._yPoints = []


    def midpoint(self, p1, p2):
        mid = (p1 + p2) / 2.
        return mid

    def generate(self, width, height, displacement, iteration):

        if iteration > 7:
            self.multiplierPlace()
            self.points()
            return

        if iteration == 1:
            self._x = []
            self._y = []

            random.seed()

            self._x.append(0.0)
            self._x.append(width)
            self._y.append(4.0 / 5.0 * height)
            self._y.append(4.0 / 5.0 * height)

        else:
            for j in range(len(self._x)-1):
                i = j + 1
                midx = self.midpoint(self._x[i], self._x[i - 1])
                midy = self.midpoint(self._y[i], self._y[i - 1])

                midy += random.uniform(0.0, 1.0) * displacement - displacement/2.

                if midy > height - 25:
                    midy = height - 25

                self._xm.append(midx)
                self._ym.append(midy)
            self._xp = self._x
            self._yp = self._y

            self._x = []
            self._y = []

            for i in range(len(self._xp)):
                self._x.append(self._xp[i])
                self._y.append(self._yp[i])

                if i < len(self._xp) - 1:
                    self._x.append(self._xm[i])
                    self._y.append(self._ym[i])

            self._xm = []
            self._ym = []
        self.generate(width, height, displacement * 2.0 / 3.0, iteration + 1)

    def draw(self, screen):
        for j in range(len(self._x)-1):
            i = j + 1
            screen.draw.line((self._x[i - 1], self._y[i - 1]), (self._x[i], self._y[i]), (255, 255, 255))

        for i in range(len(self._multipliersIndexes)):
            multi = str(self._multipliersValues[i]) + "x"
            screen.draw.line((self._x[self._multipliersIndexes[i]], self._y[self._multipliersIndexes[i]] - 1), (
            self._x[self._multipliersIndexes[i] + self._multipliersLengths[i] - 1],
            self._y[self._multipliersIndexes[i] + self._multipliersLengths[i] - 1] - 1), (255, 255, 255))
            screen.draw.line((self._x[self._multipliersIndexes[i]], self._y[self._multipliersIndexes[i]] - 2), (
            self._x[self._multipliersIndexes[i] + self._multipliersLengths[i] - 1],
            self._y[self._multipliersIndexes[i] + self._multipliersLengths[i] - 1] - 2), (255, 255, 255))
            screen.draw.text(multi, ((self._x[self._multipliersIndexes[i]] + self._x[self._multipliersIndexes[i] +
                                      self._multipliersLengths[i] - 1]) / 2.0, self._y[self._multipliersIndexes[i]] + 20), color="white")

    def points(self):
        self._xPoints = []
        self._yPoints = []

        for s in range(len(self._x)-1):
            i = s + 1
            slope = (self._y[i] - self._y[i - 1]) / (self._x[i] - self._x[i - 1])
            yPrev = self._y[i - 1]
            working = True
            j = self._x[i - 1]
            while working:
                yNew = slope + yPrev
                self._xPoints.append(round(j))
                self._yPoints.append(round(yNew))
                yPrev = yNew
                if j < self._x[i]:
                    j += 1
                else:
                    working = False

    def getXPoints(self):
        return self._xPoints

    def getYPoints(self):
        return self._yPoints

    def multiplierPlace(self):
        self._multipliersLengths = []
        self._multipliersIndexes = []
        self._multipliersValues = []

        for i in range(4):
            length = random.randint(0, 32767) % 4 + 2
            place = random.randint(0, 32767) % (len(self._x) - 4)

            while True:
                overlapped = False
                for k in range(len(self._multipliersIndexes)):
                    for l in range(len(self._multipliersLengths)):
                        for m in range(length):
                            if self._x[place + m] == self._x[self._multipliersIndexes[k] + l]:
                                overlapped = True
                                length = random.randint(0, 32767) % 4 + 2
                                place = random.randint(0, 32767) % (len(self._x) - 5)
                                break
                        if overlapped:
                            break
                    if overlapped:
                        break
                if not overlapped:
                    break

            if length == 2:
                self._multipliersValues.append(5)

            elif length == 3:
                self._multipliersValues.append(4)

            elif length == 4:
                self._multipliersValues.append(3)

            elif length == 5:
                self._multipliersValues.append(2)

            self._multipliersLengths.append(length)
            self._multipliersIndexes.append(place)

            for j in range(length):
                self._y[place + j] = self._y[place]

    def multiplierCheck(self, xpos):
        for i in range(len(self._multipliersIndexes)):
            if xpos >= self._x[self._multipliersIndexes[i]] and xpos <= self._x[self._multipliersIndexes[i] + self._multipliersLengths[i] - 1]:
                return self._multipliersValues[i]

        return 1
