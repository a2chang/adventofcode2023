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

	locs = []
	net = {}
	for line in lines[2:]:
		line = line.strip('\n')
		src, l, r = parse_line(line)
		net[src + ':L'] = l
		net[src + ':R'] = r
		locs.append(src)

	return locs, net, commands


def get_wheres1(_):
	return [ 'AAA' ]


def done1(wheres):
	return wheres[0] == 'ZZZ'


def traverse(wheres, net, commands, endcond):
	i = 0
	steps = 0
	while not endcond(wheres):
		steps = steps + 1
		c = commands[i]
		i = i + 1
		if i == len(commands):
			i = 0

		wheres = [ net.get('%s:%s' % (w, c)) for w in wheres ]
	return steps


def main():
	lines = read(test_input)

	# Part 1
	locs, net, commands = parse(lines)
	print traverse(get_wheres1(locs), net, commands, done1)

	# Part 2


if __name__ == "__main__":
	main()
