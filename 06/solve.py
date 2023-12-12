#!/usr/bin/python


import math

test_input = 'adventofcode.com_2023_day_6_input.txt'
#test_input = 'test_input.text'


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	return lines


def parse_line1(line):
	return [ eval(v) for v in line.split()[1:] ]


def parse_line2(line):
	return int(''.join(line.split()[1:]))


def solve_quadratic(a, b, c):
	discriminant = b ** 2 - 4 * a * c
	sqrt_discriminant = math.sqrt(discriminant)
	r1 = (- b - sqrt_discriminant) / ( 2 * a )
	r2 = (- b + sqrt_discriminant) / ( 2 * a )
	return r1, r2
	print math.floor(r1) + 1
	print math.ceil(r2) - 1


def main():
	lines = read(test_input)

	# Part 1
	params = tuple(zip(
				parse_line1(lines[0]),
				parse_line1(lines[1])
			 ))

	product = 1
	for time, distance in params:
		#print '%d %d' % (time, distance)

		# d = v * t
		#   = v * (time - v) > distance
		# v * time - v^2 > distance
		# v^2 - time * v + distance < 0
		r1, r2 = solve_quadratic(1, -time, distance)
		r1 = math.floor(r1) + 1
		r2 = math.ceil(r2) - 1

		product = product * int(r2 - r1 + 1)
	print product


	# Part 2
	time = parse_line2(lines[0])
	distance = parse_line2(lines[1])
	r1, r2 = solve_quadratic(1, -time, distance)
	r1 = math.floor(r1) + 1
	r2 = math.ceil(r2) - 1
	print int(r2 - r1 + 1)


if __name__ == "__main__":
	main()
