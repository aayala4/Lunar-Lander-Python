lander = Actor('rocket')
lander.pos = 600, 600

WIDTH = 1400
HEIGHT = 800

def draw():
	screen.clear()
	lander.draw()
