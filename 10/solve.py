#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_10_input.txt'
#test_input = 'test_input.text'


class Node():
	dirmap = {
		'L': 'ne',
		'F': 'es',
		'7': 'sw',
		'J': 'nw',
		'-': 'ew',
		'|': 'ns',
	}
	def __init__(self, x, y, c = '.'):
		# Character of node
		self._c = c
		# Location of node
		self.x = x
		self.y = y
		# True if there is a connection out that direction
		self.n = (c == 'J') or (c == 'L') or (c == '|')
		self.e = (c == 'F') or (c == 'L') or (c == '-')
		self.s = (c == 'F') or (c == '7') or (c == '|')
		self.w = (c == 'J') or (c == '7') or (c == '-')
		self.dirs = self.dirmap.get(c, '')
		#print self.dirs
		# Distance from start if not None
		self.d = None

	def debug(self):
		print('%s (%d, %d) - %s' % (self._c, self.x, self.y, self.dirs))

class Maze():

	def __init__(self):
		self._charmap = None
		self._map = None
		self._h = 0
		self._w = 0
		self._start = None

	def _populate_S(self):
		x, y = self._start

		node = Node(x, y)
		n = None
		if x > 0:
			n = self._map[y][x-1]
		node.w = n.e if n is not None else False
		n = None
		if x < (self._w - 1):
			n = self._map[y][x+1]
		node.e = n.w if n is not None else False
		n = None
		if y > 0:
			n = self._map[y-1][x]
		node.n = n.s if n is not None else False
		n = None
		if x < (self._h - 1):
			n = self._map[y+1][x]
		node.s = n.n if n is not None else False

		if node.n:
			node.dirs = node.dirs + 'n'
		if node.e:
			node.dirs = node.dirs + 'e'
		if node.s:
			node.dirs = node.dirs + 's'
		if node.w:
			node.dirs = node.dirs + 'w'

		self._map[y][x] = node

	def load(self, charmap):
		self._charmap = charmap
		self._h = len(charmap)
		self._w = len(charmap[0])
		self._map = [ [ None ] * self._w for i in range(self._h) ]

		y = 0
		while y < self._h:
			line = self._charmap[y]

			x = 0
			while x < self._w:
				c = line[x]
				if c == 'S':
					self._start = (x, y)
				#elif c in 'JL7F|=':
				else:
					self._map[y][x] = Node(x, y, c)

				x = x + 1
			y = y + 1
		self._populate_S()

	def traverse(self, n, v):
		dx = {
			'e' : 1,
			'w' : -1,
		}
		dy = {
			'n' : -1,
			's' : 1,
		}
		oppo = {
			'n' : 's',
			'e' : 'w',
			's' : 'n',
			'w' : 'e',
		}
		x = n.x + dx.get(v, 0)
		y = n.y + dy.get(v, 0)
		#print('A: %d - %d' % (x, y))

		n1 = self._map[y][x]
		v1 = n1.dirs.strip(oppo.get(v))
		#print('B: %d - %d' % (n1.x, n1.y))
		return n1, v1

	def find_loop(self):
		x, y = self._start
		d = 0

		n0 = self._map[y][x]
		v0 = self._map[y][x].dirs[0]
		n1 = self._map[y][x]
		v1 = self._map[y][x].dirs[1]

		while n0.d is None or n1.d is None:
			#print('%d - %d' % (n0.x, n0.y))
			n0.d = d
			n1.d = d
			d = d + 1
			n0, v0 = self.traverse(n0, v0)
			n1, v1 = self.traverse(n1, v1)

		print d - 1


	def test(self):
		x = 0
		y = 2
		n0 = self._map[y][x]
		print n0.dirs
		v = n0.dirs[0]
		n0, v = self.traverse(n0, v)
		print('%d - %d - %s' % (n0.x, n0.y, v))

		return
		for y in range(self._h):
			for x in range(self._w):
				self._map[y][x].debug()


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


def main():
	lines = read(test_input)
	maze = Maze()
	maze.load(lines)

	#maze.test()
	#return

	# Part 1
	maze.find_loop()

	# Part 2


if __name__ == "__main__":
	main()
