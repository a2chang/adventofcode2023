#!/usr/bin/python

# python makemap.py > adventofcode.com_2023_day_10_input.txt
# python ../10/solve.py
# Answer = 2x(part1) + (part2)


test_input = 'adventofcode.com_2023_day_18_input.txt'
#test_input = 'test_input.text'


class Map():

	def __init__(self):
		self._digplan = []
		self._map = []
		self._start = None
		self._w = 0
		self._h = 0

	def _find_bounds(self):
		xmin = 0
		xmax = 0
		ymin = 0
		ymax = 0
		x = 0
		y = 0

		for (dir, dist, _) in self._digplan:
			if dir == 'L':
				x = x - dist
				if x < xmin:
					xmin = x
			elif dir == 'R':
				x = x + dist
				if x > xmax:
					xmax = x
			elif dir == 'U':
				y = y - dist
				if y < ymin:
					ymin = y
			elif dir == 'D':
				y = y + dist
				if y > ymax:
					ymax = y
			last = dir
			#print('(%d,%d) %d:%d %d:%d' % (x, y, xmin, xmax, ymin, ymax))
		self._start = ( x - xmin, y - ymin )
		self._w = xmax - xmin + 1
		self._h = ymax - ymin + 1

		#print('[%d,%d] start (%s)' % (self._w, self._h, self._start) )

	def _draw_map(self):
		x, y = self._start
		self._map[y][x] = 'S'
		last = 'S'

		for (dir, dist, _) in self._digplan:
			if dir == 'R':
				if last == 'U':
					self._map[y][x] = 'F'
				elif last == 'D':
					self._map[y][x] = 'L'
				for i in range(dist):
					x = x + 1
					self._map[y][x] = '-'
			elif dir == 'L':
				if last == 'U':
					self._map[y][x] = '7'
				elif last == 'D':
					self._map[y][x] = 'J'
				for i in range(dist):
					x = x - 1
					self._map[y][x] = '-'
			elif dir == 'U':
				if last == 'R':
					self._map[y][x] = 'J'
				elif last == 'L':
					self._map[y][x] = 'L'
				for i in range(dist):
					y = y - 1
					self._map[y][x] = '|'
			elif dir == 'D':
				if last == 'R':
					self._map[y][x] = '7'
				elif last == 'L':
					self._map[y][x] = 'F'
				for i in range(dist):
					y = y + 1
					self._map[y][x] = '|'
			last = dir

		self._map[y][x] = 'S'


	def parse1(self, digplan):
		for r in digplan:
			dir, dist, col = r.split()
			self._digplan.append( (dir, eval(dist), col) )

	def parse2(self, digplan):
		for r in digplan:
			_, _, col = r.split()
			cmd = col.strip('()').replace('#','0x')
			dir = None
			if cmd[-1] == '0':
				dir = 'R'
			elif cmd[-1] == '1':
				dir = 'D'
			elif cmd[-1] == '2':
				dir = 'L'
			elif cmd[-1] == '3':
				dir = 'U'
			self._digplan.append( (dir, eval(cmd[:-1]), col) )

	def makemap(self):
		self._find_bounds()

		for y in range(self._h):
			self._map.append( [ '.' ] * self._w )

		self._draw_map()


	def dump(self):
		for y in range(self._h):
			print ''.join(self._map[y])


	def debug(self):
		for (dir, dist, _) in self._digplan:
			print('%s %d' % (dir, dist) )



def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


def main():
	lines = read(test_input)
	m = Map()
	m.parse1(lines)
	m.makemap()
	m.dump()

	#m = Map()
	#m.parse2(lines)
	#m.debug()
	#m.makemap()
	#m.dump()

	#m.test()
	#return


if __name__ == "__main__":
	main()
