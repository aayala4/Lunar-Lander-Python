lander = Actor('rocket')
lander.topleft = 0,0

WIDTH = 1400
HEIGHT = 800

ang = 0

def draw():
	screen.clear()
	lander.draw()
	lander.angle = ang

def update():
	lander.right += 2
	if lander.right >= WIDTH:
		lander.left = 0

def on_mouse_down(pos):
	if lander.collidepoint(pos):
		lander.left = 0

def on_key_down(key):
	global ang
	if key.name == 'LEFT':
		rotate(ang+13)
	elif key.name == 'RIGHT':
		rotate(ang-13)

def rotate(newAng):
	global ang
	if newAng > 90:
		ang = 90
	elif newAng < -90:
		ang = -90
	else:
		ang = newAng
	lander.angle = ang
