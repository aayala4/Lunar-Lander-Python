import pgzrun
import ship as lander
import terrain as land
import time

WIDTH = 1400
HEIGHT = 800
DIM = (WIDTH, HEIGHT)
PI = 3.1415926

class Game:
    def __init__(self):
        self.score = 0
        self.state = 1
        self.collided = 0

        self.multiplier = 1
        self.dt = .01

        self.playing = True

        self.ship = lander.Ship()

        self.terrain = land.Terrain()

        self.xVel = 0
        self.yVel = 0
        self.x = 0
        self.y = 0
        self.ang = 0
        self.gas = 0
        self.landingType = 0

        self.resetScheduled = False

    def run(self):
        self.update()
        self.draw()

    def resetGame(self):
        game.state = 2
        game.score = 0
        game.ship.setGas(750)
        self.resetLife()

    def resetLife(self):
        game.ship.setPos(100, 100)
        game.ship.setVel(50, 0)
        game.ship.setAng(0)
        game.ship.setAccMode(0)
        game.terrain.generate(WIDTH, HEIGHT, 450, 1)

        game.collided = 0
        game.multiplier = 1

        game.xTerrain = game.terrain.getXPoints()
        game.yTerrain = game.terrain.getYPoints()
        game.playing = True
        game.resetScheduled = False

    def gameOver(self):
        game.resetScheduled = False
        game.state = 1

game = Game()

def draw():
    screen.clear()
    if game.state == 1:
        screen.draw.text("LUNAR LANDER", (WIDTH / 2 - 60, HEIGHT / 2))
        screen.draw.text("Press P to play", (WIDTH / 2 - 60, HEIGHT / 2 + 20))
        screen.draw.text("Controls:", (WIDTH / 2 - 60, HEIGHT / 2 + 100))
        screen.draw.text("Left and Right Arrows: Rotate Ship", (WIDTH / 2 - 60, HEIGHT / 2 + 120))
        screen.draw.text("Up and Down Arrows: Strengthen/Weaken Thrusters", (WIDTH / 2 - 60, HEIGHT / 2 + 140))
        screen.draw.text("Q: Quit game", (WIDTH / 2 - 60, HEIGHT / 2 + 160))

    elif game.state == 2:
        game.ship.draw(screen)
        game.terrain.draw(screen)
        scoreStr = "SCORE    " + str(game.score)
        gasStr = "FUEL     " + str(int(game.gas))
        altStr = "ALTITUDE               " + str(int(HEIGHT - 10 - game.y))
        xVelStr = "HORIZONTAL SPEED       " + str(int(game.xVel))
        yVelStr = "VERTICAL SPEED         " + str(int(-game.yVel))
        screen.draw.text(scoreStr, (40, 40))
        screen.draw.text(gasStr, (40, 60))
        screen.draw.text(altStr, (WIDTH - 240, 40))
        screen.draw.text(xVelStr, (WIDTH - 240, 60))
        screen.draw.text(yVelStr, (WIDTH - 240, 80))

        if game.collided == 1:
            screen.draw.text("YOU CRASHED", (WIDTH / 2 - 40, HEIGHT / 2 - 20))
            screen.draw.text("YOU LOST 100 FUEL UNITS", (WIDTH / 2 - 40, HEIGHT / 2))
            if not game.resetScheduled:
                game.resetScheduled = True
                clock.schedule(game.resetLife, 4.0)
        elif game.collided == 2:
            if game.landingType == 1:
                screen.draw.text("GOOD LANDING", (WIDTH / 2 - 40, HEIGHT / 2 - 20))
                screen.draw.text("50 FUEL UNITS ADDED", (WIDTH / 2 - 40, HEIGHT / 2))
            elif game.landingType == 2:
                screen.draw.text("HARD LANDING", (WIDTH / 2 - 40, HEIGHT / 2 - 20))
            elif game.landingType == 3:
                screen.draw.text("YOU CRASHED", (WIDTH / 2 - 40, HEIGHT / 2 - 20))
                screen.draw.text("YOU LOST 100 FUEL UNITS", (WIDTH / 2 - 40, HEIGHT / 2))
            if not game.resetScheduled:
                game.resetScheduled = True
                clock.schedule(game.resetLife, 4.0)

    elif game.state == 3:
        game.ship.draw(screen)
        game.terrain.draw(screen)
        scoreStr = "SCORE    " + str(game.score)
        gasStr = "FUEL     " + str(int(game.gas))
        altStr = "ALTITUDE               " + str(int(HEIGHT - 10 - game.y))
        xVelStr = "HORIZONTAL SPEED       " + str(int(game.xVel))
        yVelStr = "VERTICAL SPEED         " + str(int(-game.yVel))
        screen.draw.text(scoreStr, (40, 40))
        screen.draw.text(gasStr, (40, 60))
        screen.draw.text(altStr, (WIDTH - 240, 40))
        screen.draw.text(xVelStr, (WIDTH - 240, 60))

        screen.draw.text("YOU RAN OUT OF FUEL", (WIDTH / 2, HEIGHT / 2))
        screen.draw.text("GAME OVER.", (WIDTH / 2, HEIGHT / 2 + 20))
        if not game.resetScheduled:
            game.resetScheduled = True
            clock.schedule(game.gameOver, 5.0)


def update(dt):
    game.dt = dt
    if game.state == 1:
        if keyboard.p:
            game.resetGame()

    elif game.state == 2:
        if game.playing:
            game.gas = game.ship.getGas()
            game.xVel = game.ship.getXvel()
            game.yVel = game.ship.getYvel()
            game.x = game.ship.getXpos()
            game.y = game.ship.getYpos()
            game.ang = game.ship.getAng()
            # Get the fuel, velocities, positions, and angle

            game.y = game.y + game.yVel * game.dt + .5 * 30. * game.dt * game.dt
            game.x = game.x + game.xVel * game.dt
            if game.x > WIDTH + 10:
                game.x = -10
            elif game.x < -10:
                game.x = WIDTH + 10
                # If ship goes off on the side of the screen, it is moved to the other side.

            if game.y < -50:
                game.x = 100
                game.y = 100
                game.xVel = 50
                game.yVel = 0
                game.ship.setAng(0)
                game.ship.setAccMode(0)
                # If the ship goes too high, then it is placed back at the initial spawn point

            if game.xVel >= 100:
                game.xVel = 100
            elif game.xVel <= -100:
                game.xVel = -100

            # Makes x velocity stay within - 100 and 100 inclusive

            game.yVel = game.yVel + 10. * game.dt
            # Calculate new y velocity

            game.xVel, game.yVel = game.ship.accelerate(game.xVel, game.yVel)
            # Accelerates ship

            game.ship.setPos(game.x, game.y)
            game.ship.setVel(game.xVel, game.yVel)
            # Update ship 's new velocities and position

            if keyboard.left:
                game.ship.rotate(game.ang - PI/14.)
                # Left Arrow
            elif keyboard.right:
                game.ship.rotate(game.ang + PI/14.)
                # Right Arrow
            elif keyboard.down:
                game.ship.accelerateChange(-1)
                # Down Arrow
            elif keyboard.up:
                game.ship.accelerateChange(1)
                # Up arrow
            elif keyboard.q:
                game.state = 1
                # Effectively quit program

            game.ship.hitbox()
            # Recalculates ship's hitbox

            game.collided = 0
            game.collided = game.ship.collision(game.xTerrain, game.yTerrain)
            # Checks if the ship collided with the terrain

            if game.collided == 1:
                game.playing = False
                game.score += 5
                game.ship.setGas(game.ship.getGas() - 100)
                game.gas = game.ship.getGas()
                # Crashed
            elif game.collided == 2:
                game.playing = False
                game.multiplier = game.terrain.multiplierCheck(game.ship.getXpos())
                # Checks if the ship landed on a multiplier spot

                if game.yVel < 12 and abs(game.xVel) < 25:
                    game.landingType = 1
                    game.ship.setGas(game.ship.getGas() + 50)
                    game.score += game.multiplier * 50
                    # If the user has a good landing

                elif game.yVel < 25 and abs(game.xVel) < 25:
                    game.landingType = 2
                    game.score += game.multiplier * 15
                    # If the user has a hard landing

                else:
                    game.landingType = 3
                    game.score += 5
                    game.ship.setGas(game.ship.getGas() - 100)
                game.gas = game.ship.getGas()

                    # If the user was going too fast resulting in a crash

            if game.ship.getGas() <= 0:
                game.gas = game.ship.getGas()
                game.state = 3


pgzrun.go()
