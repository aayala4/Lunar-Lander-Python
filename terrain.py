class Terrain:
	_x = ()
	_y = ()

	_xm = ()
	_ym = ()

	_xp = ()
	_yp = ()

	_multipliersValues = ()
	_multipliersLengths = ()
	_multipliersIndexes = ()
	
	_xPoints = ()
	_yPoints = ()

	def midpoint(p1, p2):
		mid = 0.0
		mid = (p1+p2)/2
		return mid

	def generate(width, height, displacment, iteration):
		midx = 0.0
		midy = 0.0
	
		if iteration > 7:
			multiplierPlace()
			points()
			return

		if iteration == 1:
			_x = ()
			_y = ()

			random.seed()

			_x.append(0.0)
			_x.append(width)
			_y.append(4.0/5.0*height)
			_y.append(4.0/5.0*height)

		else:
			for j in range(len(_x)):
				i = j+1
				midx = midpoint(_x[i], _x[i-1])
				midy = midpoint(_y[i], _y[i-1])

				midy += random.uniform(0.0, 1.0)*displacement-displacement/2

				if midy > height-25:
					midy = height-25

				_xm.append(midx)
				_ym.append(midy)
			_xp = _x
			_yp = _y

			_x = ()
			_y = ()

			for j in range(len(_xp)):
				i = j+1
				_x.append(_xp[i])
				_y.append(_xp[i])

				if i < len(_xp)-1:
					_x.append(_xm[i])
					_y.append(_ym[i])

			_xm = ()
			_ym = ()
		generate(width, height, displacement/2.0*3.0, iteration+1)

	def draw():
		multi = ""
		for j in range(len(_x)):
			i = j+1
			draw.line(_x[i-1], _y[i-1], _x[i], _y[i])
			
		for i in range(len(_multiplierIndexes)):
			multi = str(_multipliersValues[i])+"x"
			draw.line((_x[_multipliersIndexes[i]], _y[_multipliersIndexes[i]]-1), (_x[mulipliersIndexes[i]+multipliersLengths[i]-1], _y[mulipliersIndexes[i]+multipliersLengths[i]-1]-1))
			draw.line((_x[_multipliersIndexes[i]], _y[_multipliersIndexes[i]]-2), (_x[mulipliersIndexes[i]+multipliersLengths[i]-1], _y[mulipliersIndexes[i]+multipliersLengths[i]-1]-2))
			draw.text(multi, ((_x[multipliersIndexes[i]]+_x[multipliersIndexes[i]+multipliersLengths[i]-1])/2.0, _y[multipliersIndexes[i]]+20))

	def points():
		slope = 0.0
		yNew = 0.0
		yPrev = 0.0
		_xPoints = ()
		_yPoints = ()
		
		for s in range(len(_x)):
			i = s+1
			slope = (_y[i] - _y[i-1])/(_x[i]-_x[i-1])
			yPrev = _y[i-1]
			for j in range(_x[i-1], _x[i]):
				yNew = slope+yPrev
				_xPoints.append(round(j))
				_yPoints.append(round(yNew))
				yPrev = yNew

	def getXPoints():
		return _xPoints
	
	def getYPoints():
		return _yPoints

	def multiplierPlace():
		length = 0
		place = 0
		overlapped = False
		_multipliersLengths = ()
		_multipliersIndexes = ()
		_multipliersValues = ()
		doWhile = True

		for i in range(4):
			length = randint(0, 32767) % 4 + 2
			place = randint(0,32767) % (len(_x)-4)
				
			while doWhile:
				doWhile = False
				for k in range(len(_multipliersIndexes)):
					for l in range(len_multipliersLengths):
						for m in range(length):
							if _x[place+m] == _x[multipliersIndexe[k]+l]:
								doWhile = True
								length = randint(0, 32767) % 4 +2
								place = randint(0,32767) % (len(_x)-5)
								break
						if (doWhile):
							break
					if (doWhile):
						break
					
			if length == 2:
				multipliersValues.append(5)

			if length == 3:
				multipliersValues.append(4)

			if length == 4:
				multipliersValues.append(3)

			if length == 5:
				multipliersValues.append(2)

			mulipliersLengths.append(length)
			multipliersIndexes.append(place)

			for j in range(length):
				_y[place+j] = _y[place]

	def multiplierCheck(xpos):
		for i in range(len(multipliersIndexes)):
			if xpos >= _x[multipliersIndexes[i]] and xpos <= _x[multipliersIndexes[i]+multipliersLength[i]-1]:
				return multipliersValues[i]

		return 1
