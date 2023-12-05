#!/usr/bin/python


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	return lines


def find_single(substr):
	transform = {
		#'zero': '0',
		'one': '1',
		'two': '2',
		'three': '3',
		'four': '4',
		'five': '5',
		'six': '6',
		'seven': '7',
		'eight': '8',
		'nine': '9',
		'1': '1',
		'2': '2',
		'3': '3',
		'4': '4',
		'5': '5',
		'6': '6',
		'7': '7',
		'8': '8',
		'9': '9',
	}
	for k, v in transform.iteritems():
		if substr.startswith(k):
			return int(v)
	return None


def process_line_part2(line):
	line = line.strip('\n')
	#print(line)

	index = 0
	a = None
	b = None
	while (index < len(line)):
		if a is None:
			a = find_single(line[index:])
		if b is None:
			b = find_single(line[-index-1:])
		index = index + 1

	if a is not None and b is not None:
		#print('%i %i' % (a, b))
		return a*10 + b
	return 0


def process_line_part1(line):
	#print line
	line = line.strip('abcdefghijklmnopqrstuvwxyz\n')
	#print line
	a = int(line[0])
	b = int(line[-1])
	#print('%i %i' % (a, b))
	if a is not None and b is not None:
		return a*10 + b
	return 0



def main():
	lines = read('adventofcode.com_2023_day_1_input.txt')

	# Part 1
	sum = 0
	for line in lines:
		sum = sum + process_line_part1(line)
	print sum

	# Part 2
	sum = 0
	for line in lines:
		sum = sum + process_line_part2(line)
	print sum


if __name__ == "__main__":
	main()
