lander = Actor('rocket')
lander.topleft = 0,0

WIDTH = 1400
HEIGHT = 800


def draw():
	screen.clear()
	lander.draw()
	lander.angle = 0

#def update():
	#lander.right += 2
	#if lander.right >= WIDTH:
	#	lander.left = 0

def on_mouse_down(pos):
	if lander.collidepoint(pos):
		lander.left = 0

def on_key_down(key):
	if key.name == 'LEFT':
		print("landerang 2: " + str(lander.angle))
		rotate(lander.angle+13)
	elif key.name == 'RIGHT':
		print("landerang 2: " + str(lander.angle))
		rotate(lander.angle-13)

def rotate(newAng):
	print("newAng: " + str(newAng))
	if newAng > 90:
		lander.angle = 90
	elif newAng < -90:
		lander.angle = -90
	else:
		lander.angle = newAng
	print("landerang: " + str(lander.angle))
