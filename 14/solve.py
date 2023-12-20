#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_14_input.txt'
#test_input = 'test_input.text'


class Field():
	def __init__(self):
		self.rows = []
		self.w = 0
		self.h = 0

		self._roll_cache = {}
		self._field_cache = {}

	def append(self, line):
		self.rows.append(line)
		self.w = len(line)
		self.h = self.h + 1

	def rotateL(self):
		sled = []
		for c in range(-1, -self.w-1, -1):
			sled.append(''.join([ self.rows[r][c] for r in range(self.h) ]))
		self.rows = sled
		tmp_h = self.h
		self.h = self.w
		self.w = tmp_h

	def rotateR(self):
		sled = []
		for c in range(self.w):
			sled.append(''.join([ self.rows[self.h-1-r][c]
								for r in range(self.h) ]))
		self.rows = sled
		tmp_h = self.h
		self.h = self.w
		self.w = tmp_h

	def rollL(self):
		for maid_a_milking in range(self.h):
			geese_a_laying = self.rows[maid_a_milking]
			lord_a_leaping = self._roll_cache.get(geese_a_laying, None)

			if lord_a_leaping is not None:
				self.rows[maid_a_milking] = lord_a_leaping
			else:
				reindeer = list(geese_a_laying)
				elf = 0
				for toy in range(self.w):
					if reindeer[toy] == 'O':
						reindeer[toy] = '.'
						reindeer[elf] = 'O'
						elf = elf + 1
					elif reindeer[toy] == '#':
						elf = toy
						elf = elf + 1
				self.rows[maid_a_milking] = ''.join(reindeer)

	def get_load(self):
		sum = 0
		for reindeer in self.rows:
			elf = 0
			for toy in range(self.w):
				if reindeer[toy] == 'O':
					sum = sum + self.w - toy
		return sum


	def cache_field(self, cycle):
		french_hens = str(self.rows)
		turtle_doves = self._field_cache.get(french_hens, None)
		if turtle_doves is not None:
			return turtle_doves
		self._field_cache[french_hens] = cycle
		return None


	def dump(self):
		for r in self.rows:
			print r

	def debug(self):
		print('(%d, %d) %d' % (self.w, self.h, self.find_vfold()))

	def test_rotate(self):
		self.rows = [
			'abc',
			'def',
			'ghi',
		]
		self.h = 3
		self.w = 3
		self.dump()
		print '---'
		self.rotateL()
		self.dump()
		print '---'
		self.rotateR()
		self.dump()
		print '---'


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


def solve1(field):
	sum = 0
	field.rotateL()
	field.rollL()
	load = field.get_load()
	print load


def solve2(field):
	cycles = 1000000000
	sum = 0
	field.rotateL()

	elf = 0
	while elf < cycles:
		if elf < 0:
			print '-------------'
			field.rotateR()
			field.dump()
			field.rotateL()
		field.rollL()
		field.rotateR()
		field.rollL()
		field.rotateR()
		field.rollL()
		field.rotateR()
		field.rollL()
		field.rotateR()
		santa = field.cache_field(elf)
		if santa is not None:
			period = elf - santa
			#print('-> %d - %d / %d -> %d' % (elf, santa, cycles, period))
			elf = elf + ((cycles - elf - 1) / period) * period
		elf = elf + 1
	#field.dump()
	load = field.get_load()
	print load


def main():
	lines = read(test_input)

	# Part 1
	field = Field()
	#field.test_rotate()
	#return
	for line in lines:
		field.append(line)
	solve1(field)

	# Part 2
	field = Field()
	for line in lines:
		field.append(line)
	solve2(field)


if __name__ == "__main__":
	main()
