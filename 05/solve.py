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
		ret = src + self._map[self._keys[i]]

		run = None
		if (i + 1) < len(self._keys):
			run = self._keys[i + 1] - src - 1

		return ret, run

	def dump(self):
		print self._map


class Almanac():

	def __init__(self):
		self._seeds = []
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
		print self._seeds
		for k in self._maps.iterkeys():
			print k
			self._maps.get(k).dump()

	def _parse_seeds(self, line, _):
		self._seeds = [ int(v) for v in line.split()[1:] ]

	def _parse_map(self, line, mapper):
		if mapper is None:
			return
		dest, src, length = line.split(' ')
		mapper.add(int(dest), int(src), int(length))

	def map(self, mapname, val):
		return self._maps.get(mapname).map(val)

	def get_seeds1(self):
		return [ [ s, 1 ] for s in self._seeds ]

	def get_seeds2(self):
		return [ self._seeds[i:i+2] for i in range(0, len(self._seeds), 2) ]


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
		val, run = m.map(i)
		if run is not None:
			r = '%03d' % run
		print ('%03d %03d / %s' % (i, val, r))


def run_part(almanac, seed_func):
	locmin = None
	for seed0, l in seed_func():
		seed = seed0
		while seed < seed0 + l:
			v = seed
			skip = None

			for n in almanac.map_names:
				v1, run = almanac.map(n, v)
				#print n, v, v1
				v = v1
				if run is not None:
					if skip is None:
						skip = run
					elif run < skip:
						skip = run
			if locmin is None or v < locmin:
				locmin = v

			if skip is None:
				continue
			seed = seed + 1 + skip
	return locmin

def main():
	#test()
	#return

	lines = read(test_input)
	almanac = Almanac()
	almanac.parse(lines)

	# Part 1
	locmin = run_part(almanac, almanac.get_seeds1)
	print locmin

	# Part 2
	locmin = run_part(almanac, almanac.get_seeds2)
	print locmin


if __name__ == "__main__":
	main()
