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
		self.is_nexus = False

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

	@staticmethod
	def reverse(dir):
		if dir == 'n':
			return 's'
		elif dir == 's':
			return 'n'
		elif dir == 'e':
			return 'w'
		elif dir == 'w':
			return 'e'
		return None

	def __init__(self):
		self._charmap = None
		self._map = None
		self._h = 0
		self._w = 0
		self._start = None
		self._end = None
		self.neighbours = {}	# dir: (node, weight)

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
		exits = 0
		for d in 'nesw':
			n = self._get_node(x + Maze.dx[d], y + Maze.dy[d])
			if n is not None:
				if d in Maze.walkable[node.c]:
					node.neighbours[d] = (n, 1)
				if d in Maze.walkable['.']:
					exits = exits + 1
		if exits != 2:
			node.is_nexus = True

	def _link_nodes(self):
		for y in range(self._h):
			for x in range(self._w):
				self._find_neighbours(x, y)

	def load(self, charmap, ignore_slopes=False):
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
					if ignore_slopes:
						c = '.'
					self._map[y][x] = Node(x, y, c)
					if y == 0:
						self._start = (x, y)
					elif y == (self._h - 1):
						self._end = (x, y)
				x = x + 1
			y = y + 1

		self._link_nodes()

	# Return nexus and length of path starting at node
	def _trace(self, node, direction):
		#print('==== trace %d.%s' % (node.id, direction))
		dist = 0
		while node.is_nexus is False:
			#print('== %d / %d' % (node.id, dist))
			adj = node.neighbours.keys()
			if Maze.reverse(direction) in adj:
				adj.remove(Maze.reverse(direction))
			if len(adj) == 0:
				return (None, 0)
			direction = adj[0]
			(node, weight) = node.neighbours.get(direction, (None, 0))
			dist = dist + weight
		return (node, dist)

	def optimise(self):
		for y in range(self._h):
			for x in range(self._w):
				node = self._map[y][x]
				if node is not None and node.is_nexus:

					adj_list = node.neighbours.keys()
					for d in adj_list:
						(neigh, w) = node.neighbours[d]
						(target, dist) = self._trace(neigh, d)
						if target is not None:
							#print('>> Node %d.%s - %d / %d' % (node.id, d, target.id, w+dist))
							node.neighbours[d] = (target, w + dist)


	def dfs_traverse(self, node, goal, visited):
		if node.id == goal.id:
			return 0

		longest = None
		for (n, w) in node.neighbours.values():
			if n.id not in visited:
				visited.add(n.id)
				dist = self.dfs_traverse(n, goal, visited)
				if dist is not None:
					if longest is None:
						longest = dist + w
					else:
						if (dist + w) > longest:
							longest = dist + w
				visited.remove(n.id)

		return longest if longest is not None else None

	def iter_dfs_traverse(self, node, goal, _):
		node_stack = [ node ]
		visited_stack = [ str({ node.id }) ]
		length_stack = [ 0 ]

		longest = None

		while len(node_stack) > 0:
			node = node_stack.pop()
			visited_str = visited_stack.pop()
			length = length_stack.pop()

			#print('id=%d, visited=%s, len=%d' % (node.id, visited_str, length))

			if node.id == goal.id:
				if longest is None:
					longest = length
				elif length > longest:
					longest = length
			else:
				for (n, w) in node.neighbours.values():
					visited = eval(visited_str)
					if n.id not in visited:
						node_stack.append(n)
						visited.add(n.id)
						visited_stack.append(str(visited))
						length_stack.append(length + w)

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


	def dump(self):
		print('%s - %s' % (self._start, self._end))
		for y in range(self._h):
			line = ''
			for x in range(self._w):
				n = self._map[y][x]
				if n is None:
					line = line + '   '
				else:
					line = line + '%3d'%n.id
			print line


	def part1(self):
		start = self._get_node(self._start[0], self._start[1])
		end = self._get_node(self._end[0], self._end[1])
		return self.dfs_traverse(start, end, set())
		#return self.iter_dfs_traverse(start, end, set())
		


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
	#maze.dump()
	maze.optimise()
	d = maze.part1()
	print d

	maze2 = Maze()
	maze2.load(lines, True)
	#maze2.test()
	#maze2.dump()
	maze2.optimise()
	d = maze2.part1()
	print d



if __name__ == "__main__":
	main()
