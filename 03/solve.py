#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_3_input.txt'


def _debug_raw(string):
	return
	import sys
	sys.stdout.write(string)

def _debug(string):
	return
	print(string)


class Schematic:
	_map = []
	stars = {}
	width = 0
	height = 0

	def __init__(self):
		pass


	def load(self, filename):
		file1 = open(filename, 'r')
		self._map = file1.readlines()

		self._map = [ line.strip('\n') for line in self._map ]

		self.width = len(self._map[0])
		self.height = len(self._map)


	def is_in_bound(self, x, y):
		if x < 0 or x >= self.width:
			return False
		if y < 0 or y >= self.height:
			return False
		return True


	# No bounds checking
	def _is_digit(self, x, y):
		return self._map[y][x].isdigit()

	def is_digit(self, x, y):
		if not self.is_in_bound(x, y):
			return False
		return self._is_digit(x, y)

	def _add_star(self, x, y, val):
		if self._map[y][x] == '*':
			index = '%04d-%04d' % (x, y)
			m = self.stars.get(index, None)
			if m is None:
				self.stars[index] = []
			self.stars[index].append(val)

	def _is_symbol(self, x, y):
		if self._map[y][x] == '.':
			return False
		if self._is_digit(x, y):
			return False
		return True

	def is_symbol(self, x, y):
		if not self.is_in_bound(x, y):
			return False
		return self._is_symbol(x, y)


	def _has_symbol(self, x0, x1, y):
		for x in range(x0, x1):
			if self.is_symbol(x, y):
				return True
		return False

	def add_star_value(self, x0, x1, y, val):
		xx0 = x0 - 1
		if xx0 < 0:
			xx0 = 0
		xx1 = x1 + 1
		if xx1 > self.width:
			xx1 = self.width
		
		# check line y - 1
		if y > 0:
			#_debug_raw('-' + self.get_string(xx0, xx1, y+1))
			for x in range(xx0, xx1):
				self._add_star(x, y-1, val)

		if x0 > 0:
			self._add_star(x0-1, y, val)
		if x1 < self.width:
			self._add_star(x1, y, val)

		# check line y + 1
		if y < (self.height-1):
			#_debug_raw('+' + self.get_string(xx0, xx1, y+1))
			for x in range(xx0, xx1):
				self._add_star(x, y+1, val)

	def is_adjacent(self, x0, x1, y):
		xx0 = x0 - 1
		if xx0 < 0:
			xx0 = 0
		xx1 = x1 + 1
		if xx1 > self.width:
			xx1 = self.width
		
		# check line y - 1
		if y > 0:
			#_debug_raw('-' + self.get_string(xx0, xx1, y+1))
			if self._has_symbol(xx0, xx1, y-1):
				return True

		if self.is_symbol(x0 - 1, y):
			return True
		if self.is_symbol(x1, y):
			return True

		# check line y + 1
		if y < self.height:
			#_debug_raw('+' + self.get_string(xx0, xx1, y+1))
			if self._has_symbol(xx0, xx1, y+1):
				return True

		return False

	def get_string(self, x0, x1, y):
		v = self._map[y][x0:x1]
		return v

	def get_value(self, x0, x1, y):
		v = self._map[y][x0:x1]
		return int(v)

	def dump_digits(self):
		for y in range(0, self.height):
			for x in range(0, self.width):
				if self.is_digit(x, y):
					_debug_raw('*')
				else:
					_debug_raw('.')
			_debug('')

	def dump_symbols(self):
		for y in range(0, self.height):
			for x in range(0, self.width):
				if self.is_symbol(x, y):
					_debug_raw('*')
				else:
					_debug_raw('.')
			_debug('')




def main():
	schematic = Schematic()
	schematic.load(test_input)
	#_debug schematic.width
	#_debug schematic.height


	#schematic.dump_digits()
	#_debug '=============================='
	#schematic.dump_symbols()

	# Part 1
	sum = 0
	for y in range(0, schematic.height):
		x = 0
		while x < schematic.width:
			if schematic.is_digit(x, y):
				x0 = x
				x = x + 1
				while schematic.is_digit(x, y):
					x = x + 1
				x1 = x

				#val = schematic.get_value(x0, x1, y)
				#_debug_raw(' ' + str(val) + ':')

				if schematic.is_adjacent(x0, x1, y):
					val = schematic.get_value(x0, x1, y)
					sum = sum + val
					#_debug_raw(str(val) + ' ')
			x = x + 1
		#_debug ('')
	print sum


	# Part 2
	for y in range(0, schematic.height):
		x = 0
		while x < schematic.width:
			if schematic.is_digit(x, y):
				x0 = x
				x = x + 1
				while schematic.is_digit(x, y):
					x = x + 1
				x1 = x

				val = schematic.get_value(x0, x1, y)
				#_debug_raw(' ' + str(val) + ':')
				schematic.add_star_value(x0, x1, y, val)
			x = x + 1
		#_debug ('')

	sum = 0
	for star in schematic.stars.values():
		if len(star) == 2:
			sum = sum + star[0] * star[1]
	print sum



if __name__ == "__main__":
	main()
