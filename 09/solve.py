#!/usr/bin/python


import numpy


test_input = 'adventofcode.com_2023_day_9_input.txt'
#test_input = 'test_input.text'


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	return lines


def parse_line(line):
	#print line
	vals = [ eval(v) for v in line.split() ]
	n = len(vals)
	pows = []
	for i in range(n+1):
		pows.append( [ i**j for j in range(n) ] )
	#print pows
	#print vals
	arr_pows = numpy.array(pows[:-1])
	arr_vals = numpy.array(vals)

	coeffs = numpy.linalg.solve(arr_pows, arr_vals)
	#print coeffs
	arr_pows = numpy.array(pows[-1])
	n = numpy.dot(coeffs, arr_pows)
	#print n
	return n
	


def parse(lines):
	sum = 0
	for line in lines:
		line = line.strip('\n')
		sum = sum + parse_line(line)
	print sum


def main():
	lines = read(test_input)

	# Part 1
	parse(lines)

	# Part 2
	#parse(lines, True)


if __name__ == "__main__":
	main()
