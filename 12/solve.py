#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_12_input.txt'
#test_input = 'test_input.text'


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


# . is operational
# # is damaged
def get_signature(pattern):
	state = None
	count = 0
	sig = []
	for c in pattern:
		if c != '.':
			count = count + 1
		else:
			if state != '.':
				if count > 0:
					sig.append(count)
				count = 0
		state = c
	if count > 0:
		sig.append(count)
	return sig


def get_wcs(pattern):
	# Find wildcards
	wcs = []
	i = 0
	while i < len(pattern):
		if pattern[i] == '?':
			wcs.append(i)
		i = i + 1
	return wcs


def get_iteration(array, wcs, iter):
	for i in range(len(wcs)):
		array[wcs[i]] = '#' if (iter & (1 << i)) else '.'
	s = ''.join(array)
	#print s
	return s


def iterate(pattern, wcs, signature):
	#print '------------------- %s' % signature
	matches = 0
	array = list(pattern)
	for i in range(2**len(wcs)):
		pat = get_iteration(array, wcs, i)
		sig = get_signature(pat)
		#print sig
		if sig == signature:
			matches = matches + 1
	return matches


def parse(line):
	pattern, s = line.split()
	signature = s.split(',')
	signature = [ eval(s) for s in signature ]
	#print pattern
	#print signature

	# Find wildcards
	wcs = get_wcs(pattern)

	# Iterate through all possible wildcard combinations
	return iterate(pattern, wcs, signature)


def main():
	lines = read(test_input)

	#maze.test()
	#return

	# Part 1
	sum = 0
	for line in lines:
		sum = sum + parse(line)
	print sum

	# Part 2
	#maze.find_area()


if __name__ == "__main__":
	main()
