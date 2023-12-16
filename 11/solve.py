#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_11_input.txt'
#test_input = 'test_input.text'


class Chart():

	def __init__(self):
		self._charmap = None
		self._h = 0
		self._w = 0
		self._galaxies = []

	def load(self, charmap):
		self._charmap = charmap
		self._h = len(charmap)
		self._w = len(charmap[0])
		self._hdist1 = [ 2 ] * self._w
		self._vdist1 = [ 2 ] * self._h
		self._hdist2 = [ 1000000 ] * self._w
		self._vdist2 = [ 1000000 ] * self._h

		y = 0
		while y < self._h:
			line = self._charmap[y]

			x = 0
			while x < self._w:
				c = line[x]
				if c == '#':
					self._hdist1[x] = 1
					self._vdist1[y] = 1
					self._hdist2[x] = 1
					self._vdist2[y] = 1
					self._galaxies.append( (x, y) )

				x = x + 1
			y = y + 1


	def get_dist(self, i0, i1, intervals):
		return sum(intervals[i0:i1])


	def dist(self, g0, g1, hdist, vdist):
		x0, y0 = g0
		x1, y1 = g1
		d = 0

		if x0 < x1:
			d = d + self.get_dist(x0, x1, hdist)
		else:
			d = d + self.get_dist(x1, x0, hdist)

		if y0 < y1:
			d = d + self.get_dist(y0, y1, vdist)
		else:
			d = d + self.get_dist(y1, y0, vdist)

		return d


	def partial(self, hdist, vdist):
		sum = 0
		num_galaxies = len(self._galaxies)
		for i in range(num_galaxies):
			g0 = self._galaxies[i]
			for j in range(i+1, num_galaxies):
				g1 = self._galaxies[j]
				sum = sum + self.dist(g0, g1, hdist, vdist)
		print sum


	def part1(self):
		self.partial(self._hdist1, self._vdist1)


	def part2(self):
		self.partial(self._hdist2, self._vdist2)


	def test(self):
		print self._hdist1
		print self._vdist1
		for x, y in self._galaxies:
			print('galaxy %d-%d' % (x, y))


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


def main():
	lines = read(test_input)
	chart = Chart()
	chart.load(lines)

	#chart.test()
	#return

	# Part 1
	chart.part1()

	# Part 2
	chart.part2()


if __name__ == "__main__":
	main()
