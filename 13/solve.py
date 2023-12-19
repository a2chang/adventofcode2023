#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_13_input.txt'
#test_input = 'test_input.text'


class Field():
	def __init__(self):
		self.rows = []
		self.w = 0
		self.h = 0
		self.MAX_DIFF = 0

	def set_max_diff(self, max_diff):
		self.MAX_DIFF = max_diff

	def append(self, line):
		self.rows.append(line)
		self.w = len(line)
		self.h = self.h + 1

	def transpose(self, f):
		for c in range(f.w):
			self.rows.append(''.join([ f.rows[r][c] for r in range(f.h) ]))
		self.h = f.w
		self.w = f.h
		self.MAX_DIFF = f.MAX_DIFF


	def _diff_rows(self, r0, r1):
		d = 0
		for x, y in zip(self.rows[r0], self.rows[r1]):
			if x != y:
				d = d + 1
				# Max diff we care about - if there count exceeds that, bail
				if d > self.MAX_DIFF:
					return d
		return d


	def is_vfold(self, row):
		r0 = row
		r1 = row + 1
		diffs = 0
		while (r0 >= 0) and (r1 < self.h):
			diffs = diffs + self._diff_rows(r0, r1)
			if diffs > self.MAX_DIFF:
				return False
			r0 = r0 - 1
			r1 = r1 + 1
		return diffs == self.MAX_DIFF

	def find_hfold(self):
		f = Field()
		f.transpose(self)
		return f.find_vfold()

	def find_vfold(self):
		for r in range(self.h - 1):
			if self.is_vfold(r):
				return r + 1
		return None

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


def solve(fields, diffs = 0):
	sum = 0
	for f in fields:
		f.set_max_diff(diffs)
		#f.debug()
		r = f.find_vfold()
		if r is not None:
			sum = sum + r * 100
		else:
			c = f.find_hfold()
			sum = sum + c
	print sum


def main():
	lines = read(test_input)

	fields = []
	field = None

	for line in lines:
		if line == '':
			fields.append(field)
			field = None
		else:
			if field == None:
				field = Field()
			field.append(line)
	if field is not None:
		fields.append(field)

	# Part 1
	solve(fields, 0)

	#f = fields[0]
	#f.dump()
	#print '---'
	#f2 = Field()
	#f2.transpose(f)
	#f2.dump()

	# Part 2
	solve(fields, 1)


if __name__ == "__main__":
	main()
