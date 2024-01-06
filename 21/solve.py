#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_21_input.txt'
#test_input = 'test_input.text'


class Map():
	uncharted = None
	unvisited = -1
	rock = -2

	def __init__(self):
		self._map = None
		self._h = 0
		self._w = 0
		self._start = None

	def load(self, lines):
		self._h = len(lines)
		self._w = len(lines[0])
		self._map = [ [ None ] * self._w for i in range(self._h) ]

		y = 0
		while y < self._h:
			line = lines[y]

			x = 0
			while x < self._w:
				c = line[x]
				if c == 'S':
					self._start = (x, y)
					self._map[y][x] = 0
				elif c == '.':
					self._map[y][x] = Map.unvisited
				elif c == '#':
					self._map[y][x] = Map.rock

				x = x + 1
			y = y + 1

	def _walk(self, x, y, d):
		if (x < 0) or (x >= self._w):
			return False
		if (y < 0) or (y >= self._h):
			return False
		if self._map[y][x] != Map.unvisited:
			return False
		self._map[y][x] = d
		return True

	def find_distances(self):
		done = False
		d = 0
		squares = [ self._start ]
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

	def count_by_dist(self, d):
		count = 0
		for y in range(self._h):
			for x in range(self._w):
				dist = self._map[y][x]
				if (dist >= 0) and (dist <= d) and ((dist & 1) == (d & 1)):
					count = count + 1
		return count
		
	def debug(self, d):
		(x0, y0) = self._start
		print('%d / %d : %d / %d' % (x0, self._w, y0, self._h))
		for y in range(self._h):
			line = ''
			line2 = ''
			for x in range(self._w):
				dist = self._map[y][x]
				#if (x != x0) and (y != y0):
				#	line = line + ' '
				if (dist >= 0) and (dist <= d) and ((dist & 1) == (d & 1)):
					line = line + 'O'
				elif dist == Map.rock:
					line = line + '#'
				else:
					line = line + '.'
				line2 = line2 + '%4d' % dist
			print line2
		


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


def main():
	lines = read(test_input)
	garden = Map()
	garden.load(lines)
	garden.find_distances()

	#garden.debug(10)

	c = garden.count_by_dist(64)
	print c


if __name__ == "__main__":
	main()
