#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_21_input.txt'
#test_input = 'test_input.text'
#test_input = 'test_input2.text'


class Tile():
	uncharted = None
	unvisited = -1
	rock = -2

	def __init__(self):
		self._map = None
		self.h = 0
		self.w = 0
		self.start = None
		self.evens = 0
		self.odds = 0

	def load(self, lines):
		self.h = len(lines)
		self.w = len(lines[0])
		self._map = [ [ None ] * self.w for i in range(self.h) ]

		y = 0
		while y < self.h:
			line = lines[y]

			x = 0
			while x < self.w:
				c = line[x]
				if c == 'S':
					self.start = (x, y)
					self._map[y][x] = 0
				elif c == '.':
					self._map[y][x] = Tile.unvisited
				elif c == '#':
					self._map[y][x] = Tile.rock

				x = x + 1
			y = y + 1

	def _walk(self, x, y, d):
		if (x < 0) or (x >= self.w):
			return False
		if (y < 0) or (y >= self.h):
			return False
		if self._map[y][x] != Tile.unvisited:
			return False

		self._map[y][x] = d
		if (d & 1) == 1:
			self.odds = self.odds + 1
		else:
			self.evens = self.evens + 1
		return True

	def set_start(self, x, y):
		(x0, y0) = self.start
		self._map[y0][x0] = Tile.unvisited
		self.start = (x, y)
		self._map[y][x] = 0

	def find_distances(self):
		done = False
		d = 0
		squares = [ self.start ]
		self.evens = self.evens + 1
		while len(squares) > 0:
			prochaine = []
			for (x, y) in squares:
				if self._walk(x-1, y, d+1):
					prochaine.append( (x-1, y) )
				if self._walk(x+1, y, d+1):
					prochaine.append( (x+1, y) )
				if self._walk(x, y-1, d+1):
					prochaine.append( (x, y-1) )
				if self._walk(x, y+1, d+1):
					prochaine.append( (x, y+1) )
			squares = prochaine
			d = d + 1

	def count_by_dist(self, d, debug=False):
		count = 0
		for y in range(self.h):
			for x in range(self.w):
				dist = self._map[y][x]
				if (dist >= 0) and (dist <= d) and ((dist & 1) == (d & 1)):
					count = count + 1
		if debug:
			print('Dist: %d - %d' % (d, count))
		return count
		
	def debug(self, d, full):
		(x0, y0) = self.start
		print('start: %d, %d   size: %d, %d' % (x0, y0, self.w, self.h))
		print('odds:%d   evens:%s' % (self.odds, self.evens))
		if not full:
			return
		for y in range(self.h):
			line = ''
			line2 = ''
			for x in range(self.w):
				dist = self._map[y][x]
				#if (x != x0) and (y != y0):
				#	line = line + ' '
				if (dist >= 0) and (dist <= d) and ((dist & 1) == (d & 1)):
					line = line + 'O'
				elif dist == Tile.rock:
					line = line + '#'
				else:
					line = line + '.'
				line2 = line2 + '%4d' % dist
			print line2

#------------------------------------------------------------------------------
def part2(lines, distance, debug=False):
	lines = read(test_input)
	garden = Tile()
	garden.load(lines)
	garden.find_distances()

	ee = Tile()
	ee.load(lines)
	ee.set_start(garden.w - 1, garden.start[1])
	ee.find_distances()

	ss = Tile()
	ss.load(lines)
	ss.set_start(garden.start[0], garden.h - 1)
	ss.find_distances()

	ww = Tile()
	ww.load(lines)
	ww.set_start(0, garden.start[1])
	ww.find_distances()

	nn = Tile()
	nn.load(lines)
	nn.set_start(garden.start[0], 0)
	nn.find_distances()

	ne = Tile()
	ne.load(lines)
	ne.set_start(garden.w - 1, 0)
	ne.find_distances()

	se = Tile()
	se.load(lines)
	se.set_start(garden.w - 1, garden.h - 1)
	se.find_distances()

	sw = Tile()
	sw.load(lines)
	sw.set_start(0, garden.h - 1)
	sw.find_distances()

	nw = Tile()
	nw.load(lines)
	nw.set_start(0, 0)
	nw.find_distances()

	d = distance
	w = garden.w
	w0 = w >> 1
	nx = (d - w0) / w
	rx = d - w0 - nx*w
	if debug:
		print('d=%d  w=%d  w0=%d  nx=%d  rx=%d' % (d, w, w0, nx, rx))

	h0 = garden.h >> 1

	if (d & 1) == 1:
		tile_count0 = garden.odds
		tile_count1 = garden.evens
	else:
		tile_count0 = garden.evens
		tile_count1 = garden.odds
	if debug:
		print('tile_count %d/%d' % (tile_count0, tile_count1))

	d_axis1 = rx - 1
	d_axis2 = d_axis1 + w
	d_corner1 = d_axis1 - h0 - 1
	d_corner2 = d_corner1 + w
	d_corner3 = d_corner2 + w
	if debug:
		print('d_axis1 = %d' % d_axis1)
		print('d_axis2 = %d' % d_axis2)
		print('d_corner1 = %d' % d_corner1)
		print('d_corner2 = %d' % d_corner2)
		print('d_corner3 = %d' % d_corner3)

	# Getting lazy - assuming w = h, w0 = h0
	count = 0
	if nx < 0:
		if debug:
			print('if nx < 0:')
		count = count + garden.count_by_dist(d)
	elif nx == 0:
		if debug:
			print('elif nx == 0:')
		count = count + ee.count_by_dist(d_axis1)
		count = count + ss.count_by_dist(d_axis1)
		count = count + ww.count_by_dist(d_axis1)
		count = count + nn.count_by_dist(d_axis1)

		count = count + garden.count_by_dist(d)
	elif rx > h0:
		if debug:
			print('elif rx > h0:')
		count = count + ee.count_by_dist(d_axis1)
		count = count + ss.count_by_dist(d_axis1)
		count = count + ww.count_by_dist(d_axis1)
		count = count + nn.count_by_dist(d_axis1)

		count = count + (nx + 1) * se.count_by_dist(d_corner1)
		count = count + (nx + 1) * sw.count_by_dist(d_corner1)
		count = count + (nx + 1) * nw.count_by_dist(d_corner1)
		count = count + (nx + 1) * ne.count_by_dist(d_corner1)
		count = count + (nx) * se.count_by_dist(d_corner2)
		count = count + (nx) * sw.count_by_dist(d_corner2)
		count = count + (nx) * nw.count_by_dist(d_corner2)
		count = count + (nx) * ne.count_by_dist(d_corner2)

		c1 = (nx & ~1) + 1
		o1 = (nx + 1) & ~1
		count = count + c1 * c1 * tile_count0
		count = count + o1 * o1 * tile_count1
	elif rx >= 0:
		if debug:
			print('elif rx >= 0:')
		count = count + ee.count_by_dist(d_axis1)
		count = count + ss.count_by_dist(d_axis1)
		count = count + ww.count_by_dist(d_axis1)
		count = count + nn.count_by_dist(d_axis1)
		if debug:
			print count

		count = count + ee.count_by_dist(d_axis2)
		count = count + ss.count_by_dist(d_axis2)
		count = count + ww.count_by_dist(d_axis2)
		count = count + nn.count_by_dist(d_axis2)
		if debug:
			print count

		count = count + (nx) * se.count_by_dist(d_corner2)
		count = count + (nx) * sw.count_by_dist(d_corner2)
		count = count + (nx) * nw.count_by_dist(d_corner2)
		count = count + (nx) * ne.count_by_dist(d_corner2)
		if debug:
			print count
		count = count + (nx - 1) * se.count_by_dist(d_corner3)
		count = count + (nx - 1) * sw.count_by_dist(d_corner3)
		count = count + (nx - 1) * nw.count_by_dist(d_corner3)
		count = count + (nx - 1) * ne.count_by_dist(d_corner3)
		if debug:
			print count

		c1 = ((nx - 1) & ~1) + 1
		o1 = nx & ~1
		count = count + c1 * c1 * tile_count0
		if debug:
			print count
		count = count + o1 * o1 * tile_count1
		if debug:
			print count
	else:
		if debug:
			print('else:')
		count = garden.count_by_dist(d)
	return count

#------------------------------------------------------------------------------


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


def main():
	lines = read(test_input)
	garden = Tile()
	garden.load(lines)
	garden.find_distances()

	#garden.debug(10, False)
	#garden.debug(10, True)

	# Part 1
	c = garden.count_by_dist(64)
	print c

	c = part2(lines, 26501365)
	print c

	return
	for d in range(5, 15, 2):
		c = part2(lines, d)
		print c


if __name__ == "__main__":
	main()
