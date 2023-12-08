#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_4_input.txt'


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	return lines


def parse_line(line):
	#print line
	_, x = line.split(':')
	b, c = x.split('|')
	winners = b.split()
	picks = c.split()

	winners.sort()
	picks.sort()

	if len(winners) == 0 or len(picks) == 0:
		return 0

	w = winners.pop()
	p = picks.pop()

	count = 0
	while True:
		if w == p:
			count = count + 1
		if p > w:
			if len(picks) == 0:
				break
			p = picks.pop()
		else:
			if len(winners) == 0:
				break
			w = winners.pop()

	if count > 0:
		return 2**(count-1)
	return 0


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
