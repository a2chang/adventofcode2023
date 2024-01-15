#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_23_input.txt'
#test_input = 'test_input.text'


class Node():
	_lastid = 1

	def __init__(self, x, y, c = '.'):
		self.id = Node._lastid
		Node._lastid = Node._lastid + 1
		# Character of node
		self.c = c
		# Location of node
		self.x = x
		self.y = y
		self.neighbours = {}

	def debug(self):
		print('%s (%d, %d) - %s' % (self.c, self.x, self.y, self.dirs))

class Maze():
	wall = '#'
	walkable = {
		'.':	'nsew',
		'^':	'n',
		'>':	'e',
		'v':	's',
		'<':	'w',
	}
	dx = {
		'e' : 1,
		'w' : -1,
		'n' : 0,
		's' : 0,
	}
	dy = {
		'n' : -1,
		's' : 1,
		'e' : 0,
		'w' : 0,
	}

	def __init__(self):
		self._charmap = None
		self._map = None
		self._h = 0
		self._w = 0
		self._start = None
		self._end = None
		self.neighbours = {}

	def _get_node(self, x, y):
		if (x < 0) or (x >= self._w):
			return None
		if (y < 0) or (y >= self._h):
			return None
		return self._map[y][x]

	def _find_neighbours(self, x, y):
		node = self._map[y][x]
		if node is None:
			return
		for d in 'nesw':
			if d in Maze.walkable[node.c]:
				n = self._get_node(x + Maze.dx[d], y + Maze.dy[d])
				if n is not None:
					node.neighbours[d] = n

	def _link_nodes(self):
		for y in range(self._h):
			for x in range(self._w):
				self._find_neighbours(x, y)

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
				if c in Maze.walkable:
					self._map[y][x] = Node(x, y, c)
					if y == 0:
						self._start = (x, y)
					elif y == (self._h - 1):
						self._end = (x, y)
				x = x + 1
			y = y + 1

		self._link_nodes()

	def dfs_traverse(self, node, goal, visited):
		if node.id == goal.id:
			return 0

		longest = None
		for n in node.neighbours.values():
			if n.id not in visited:
				visited.add(n.id)
				dist = self.dfs_traverse(n, goal, visited)
				if longest is None:
					longest = dist
				elif dist is not None:
					if dist > longest:
						longest = dist
				visited.remove(n.id)

		return longest + 1 if longest is not None else None

	def iter_dfs_traverse(self, node, goal, _):
		node_stack = [ node ]
		visited_stack = [ str({ node.id }) ]
		length_stack = [ 0 ]

		longest = None

		while len(node_stack) > 0:
			node = node_stack.pop()
			visited_str = visited_stack.pop()
			#visited = eval(visited_stack.pop())
			length = length_stack.pop()

			#print('id=%d, visited=%s, len=%d' % (node.id, visited_str, length))

			if node.id == goal.id:
				if longest is None:
					longest = length
				elif length > longest:
					longest = length
			else:
				for n in node.neighbours.values():
					visited = eval(visited_str)
					if n.id not in visited:
						node_stack.append(n)
						visited.add(n.id)
						visited_stack.append(str(visited))
						length_stack.append(length + 1)

		return longest


	def test(self):
		print('%s - %s' % (self._start, self._end))
		for y in range(self._h):
			line = ''
			for x in range(self._w):
				n = self._map[y][x]
				if n is None:
					line = line + ' '
				else:
					line = line + n.c
			print line


	def part1(self):
		start = self._get_node(self._start[0], self._start[1])
		end = self._get_node(self._end[0], self._end[1])
		#return self.dfs_traverse(start, end, set())
		return self.iter_dfs_traverse(start, end, set())
		


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

	d = maze.part1()
	print d



if __name__ == "__main__":
	main()
