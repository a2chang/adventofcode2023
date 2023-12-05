#!/usr/bin/python


import re


test_input = 'adventofcode.com_2023_day_2_input.txt'
cubes = {
	'red' : 12,
	'green' : 13,
	'blue' : 14,
}


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	return lines


def parse_line(line):
	#print line
	game, raw = line.split(':')
	_, id = game.split()
	#print id
	batches = re.split(',|;', raw)
	#print batches
	for batch in batches:
		#print batch
		count, col = batch.strip().split(' ')
		#print col
		#print count
		#print cubes.get(col, 0)
		if int(count) > cubes.get(col, 0):
			return 0
	return int(id)


def main():
	lines = read(test_input)

	# Part 1
	sum = 0
	for line in lines:
		line = line.strip('\n')
		sum = sum + parse_line(line)
	print sum

	# Part 2


if __name__ == "__main__":
	main()
