lander = Actor('rocket')
lander.topleft = 0,0

WIDTH = 1400
HEIGHT = 800

def draw():
	screen.clear()
	lander.draw()

def update():
	lander.right += 2
	if lander.right >= WIDTH:
		lander.left = 0

def on_mouse_down(pos):
	if lander.collidepoint(pos):
		lander.left = 0
