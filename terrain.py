import random

# Terrain class
class Terrain:
    # Initialize terrain vecotrs
    def __init__(self):
        # Vectors of draw point x and y positions. Used for drawing terrain lines rather than containing all points
        self._x = []
        self._y = []

        # Vectors of midpoint positions
        self._xm = []
        self._ym = []

        # Vectors of previous iteration draw point x and y positions
        self._xp = []
        self._yp = []

        # Vector holding multipliers for multiplier spots (i.e. 2, 3, 4, 5)
        self._multipliersValues = []

        # Vector holding lengths of multiplier spots
        self._multipliersLengths = []

        # Vector holding indices of _x and _y vectors where multiplier spots are
        self._multipliersIndexes = []

        # Vectors of x and y points of the terrain
        # These are different from the vectors _x and _y because these contain the actual points for the terrain
        # Used for collision detection by ship
        self._xPoints = []
        self._yPoints = []

    # Calculate average of two numbers. Used for finding midpoints
    def midpoint(self, p1, p2):
        mid = (p1 + p2) / 2.
        return mid

    # Randomly generates a terrain
    def generate(self, width, height, displacement, iteration):

        # Base case. This also calls the functions which generate the actual x and y points and the multipliers
        if iteration > 7:
            self.multiplierPlace()
            self.points()
            return

        # Initializes random seed and the _x and _y vectors to have end points at same height
        if iteration == 1:
            self._x = []
            self._y = []

            random.seed()

            self._x.append(0.0)
            self._x.append(width)
            self._y.append(4.0 / 5.0 * height)
            self._y.append(4.0 / 5.0 * height)

        else:
            #  Calculate intermediate x and y points
            for j in range(len(self._x)-1):
                i = j + 1

                # Calculate the x and y midpoints
                midx = self.midpoint(self._x[i], self._x[i - 1])
                midy = self.midpoint(self._y[i], self._y[i - 1])

                # Varies the midpoint height by changing it by a random number between -displacement and displacement.
                midy += random.uniform(0.0, 1.0) * displacement - displacement/2.

                # Makes it so the terrain can't be lower than 25 pixels from the bottom of the height
                if midy > height - 25:
                    midy = height - 25

                self._xm.append(midx)
                self._ym.append(midy)

            # Set previous iteration vectors to current _x and _y vectors
            self._xp = self._x
            self._yp = self._y

            self._x = []
            self._y = []

            # Rebuild _x and _y vectors in order from the previous iteration vectors and intermidate vectors
            for i in range(len(self._xp)):
                self._x.append(self._xp[i])
                self._y.append(self._yp[i])

                if i < len(self._xp) - 1:
                    self._x.append(self._xm[i])
                    self._y.append(self._ym[i])

            self._xm = []
            self._ym = []

        # Recursively generate more terrain points with a smaller displacement
        self.generate(width, height, displacement * 2.0 / 3.0, iteration + 1)

    # Draw the terrain
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
                                      self._multipliersLengths[i] - 1]) / 2.0-8, self._y[self._multipliersIndexes[i]] + 15), fontsize = 16, fontname="dylova")

    # Calculate actual x and y points for collision detection
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

    # Get x points
    def getXPoints(self):
        return self._xPoints

    # Get y points
    def getYPoints(self):
        return self._yPoints

    # Places multipliers on terrain
    def multiplierPlace(self):
        self._multipliersLengths = []
        self._multipliersIndexes = []
        self._multipliersValues = []

        for i in range(4):
            # Calculates length as a random number between 2 and 5
            length = random.randint(0, 32767) % 4 + 2

            # Calculates place as random index between 0 and 5th to last index of x
            # This ensures that the multipliers stay within the terrain previously generated
            place = random.randint(0, 32767) % (len(self._x) - 4)

            # This checks if the multiplier was placed on top of an already existing multiplier. If so, reroll place.
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

            # The smaller the length is, the larger the value of the multiplier
            if length == 2:
                self._multipliersValues.append(5)

            elif length == 3:
                self._multipliersValues.append(4)

            elif length == 4:
                self._multipliersValues.append(3)

            elif length == 5:
                self._multipliersValues.append(2)

            # Adds length and place to _multipliersLengths and _multipliersIndexes vectors respectively
            self._multipliersLengths.append(length)
            self._multipliersIndexes.append(place)

            # Flattens the multiplier spot
            for j in range(length):
                self._y[place + j] = self._y[place]

    # Checks given ship x position and returns a multiplier accordingly
    # If the ship landed within the x range of a multiplier spot, that multiplier is returned.
    # Otherwise, 1 is returned.
    def multiplierCheck(self, xpos):
        for i in range(len(self._multipliersIndexes)):
            if xpos >= self._x[self._multipliersIndexes[i]] and xpos <= self._x[self._multipliersIndexes[i] + self._multipliersLengths[i] - 1]:
                return self._multipliersValues[i]

        return 1
