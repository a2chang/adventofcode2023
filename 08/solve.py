#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_8_input.txt'
#test_input = 'test_input.text'


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	return lines


def parse_line(line):
	line = line.replace('=', '')
	line = line.replace('(', '')
	line = line.replace(',', '')
	line = line.replace(')', '')
	return line.split()


def parse(lines):
	commands = lines[0].strip('\n')

	net = {}
	for line in lines[2:]:
		line = line.strip('\n')
		src, l, r = parse_line(line)
		net[src + ':L'] = l
		net[src + ':R'] = r

	return net, commands


def traverse(loc, net, commands):
	i = 0
	steps = 0
	while loc != 'ZZZ':
		steps = steps + 1
		c = commands[i]
		i = i + 1
		if i == len(commands):
			i = 0

		loc = net.get('%s:%s' % (loc, c))
	return steps


def main():
	lines = read(test_input)

	# Part 1
	net, commands = parse(lines)
	print traverse('AAA', net, commands)

	# Part 2


if __name__ == "__main__":
	main()
