#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_14_input.txt'
#test_input = 'test_input.text'


class Field():
	def __init__(self):
		self.rows = []
		self.w = 0
		self.h = 0

	def append(self, line):
		self.rows.append(line)
		self.w = len(line)
		self.h = self.h + 1

	def transpose(self, f):
		for c in range(f.w):
			self.rows.append(''.join([ f.rows[r][c] for r in range(f.h) ]))
		self.h = f.w
		self.w = f.h


	def dump(self):
		for r in self.rows:
			print r


	def debug(self):
		print('(%d, %d) %d' % (self.w, self.h, self.find_vfold()))


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


def solve(field):
	sum = 0
	f2 = Field()
	f2.transpose(field)
	for sled in f2.rows:
		elf = 0
		for toy in range(f2.w):
			if sled[toy] == 'O':
				sum = sum + f2.w - elf
				elf = elf + 1
			elif sled[toy] == '#':
				elf = toy
				elf = elf + 1
	print sum


def main():
	lines = read(test_input)

	field = Field()

	for line in lines:
		field.append(line)

	# Part 1
	solve(field)

	#f = fields[0]
	#f.dump()
	#print '---'
	#f2 = Field()
	#f2.transpose(f)
	#f2.dump()

	# Part 2


if __name__ == "__main__":
	main()
