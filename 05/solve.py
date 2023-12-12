#!/usr/bin/python


import collections


test_input = 'adventofcode.com_2023_day_5_input.txt'
#test_input = 'test_input.text'


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	return lines


class Mapper():

	def __init__(self):
		self._kmin = 0
		self._map = { 0: 0 }
		self._keys = None

	def add(self, dest, src, length):
		if self._keys is not None:
			return None

		if src < self._kmin:
			self._kmin = src

		src1 = src + length
		delta = dest - src
		self._map[src] = delta
		#print ('%012d %012d %012d' % (src, src1, delta))
		if self._map.get(src1, None) is None:
			self._map[src1] = 0
		#print self._map

	def map(self, src):
		if self._keys is None:
			self._keys = [ k for k in self._map.iterkeys() ]
			self._keys.sort()

		if src < self._kmin:
			return None

		i = len(self._keys) - 1
		k = self._keys[i]
		while src < k:
			i = i - 1
			k = self._keys[i]
		return src + self._map[self._keys[i]]

	def dump(self):
		print self._map


class Almanac():

	def __init__(self):
		self.seeds = []
		self.map_names = [
			'seed-to-soil',
			'soil-to-fertilizer',
			'fertilizer-to-water',
			'water-to-light',
			'light-to-temperature',
			'temperature-to-humidity',
			'humidity-to-location',
		]
		self._maps = { n : Mapper() for n in self.map_names }
		self._last_map_name = ''

	def parse(self, lines):
		parser = self._parse_seeds
		mapper = None
		for line in lines:
			line = line.strip('\n')
			if line == '':
				continue
			elif line.endswith('map:'):
				parser = self._parse_map
				self._last_map_name, _ = line.split(' ')
				mapper = self._maps.get(self._last_map_name)
			else:
				#print self._last_map_name
				parser(line, mapper)
		#self.debug()

	def debug(self):
		print self.seeds
		for k in self._maps.iterkeys():
			print k
			self._maps.get(k).dump()

	def _parse_seeds(self, line, _):
		self.seeds = [ int(v) for v in line.split()[1:] ]

	def _parse_map(self, line, mapper):
		if mapper is None:
			return
		dest, src, length = line.split(' ')
		mapper.add(int(dest), int(src), int(length))

	def map(self, mapname, val):
		return self._maps.get(mapname).map(val)


def test():
	m = Mapper()
	m.add(50, 98, 2)
	m.add(52, 50, 48)
	m.dump()

	m2 = Mapper()
	m2.add(50, 20, 2)
	m2.add(52, 30, 5)
	m2.dump()

	m.dump()

	for i in range(150):
		print ('%03d %03d' % (i, m.map(i)))


def main():
	#test()
	#return

	lines = read(test_input)
	almanac = Almanac()
	almanac.parse(lines)

	# Part 1
	locmin = None
	for v in almanac.seeds:
		for n in almanac.map_names:
			v1 = almanac.map(n, v)
			#print n, v, v1
			v = v1
		if locmin is None or v < locmin:
			locmin = v
	print locmin

	# Part 2


if __name__ == "__main__":
	main()
