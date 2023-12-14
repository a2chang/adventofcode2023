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


def get_starts1(_):
	return [ 'AAA' ]

def done1(where):
	return where == 'ZZZ'


def get_starts2(locs):
	return [ l for l in locs if l[2] == 'A' ]

def done2(where):
	return where[2] == 'Z'


def traverse(start, net, commands, endcond):
	i = 0
	where = start
	steps = 0
	while not endcond(where):
		steps = steps + 1
		c = commands[i]
		i = i + 1
		if i == len(commands):
			i = 0

		#print where
		where = net.get('%s:%s' % (where, c))
	return steps


def traverse_cycle(start, net, commands, endcond):
	i = 0
	mod = 0
	where = start
	end = []
	visited = {''}
	while not ((mod == 0) and where in visited):
		if mod == 0:
			visited.add(where)
		c = commands[mod]
		where = net.get('%s:%s' % (where, c))
		i = i + 1
		mod = i % len(commands)
		if done2(where):
			end.append(i)
	return end


def check_end(n, ends):
	for e in ends:
		if ((n-1) % e[-1]) + 1 not in e:
			return False
	return True

def main():
	lines = read(test_input)
	locs, net, commands = parse(lines)

	# Part 1
	print traverse(get_starts1(locs)[0], net, commands, done1)

	# Part 2
	ends = []
	for s in get_starts2(locs):
		end = traverse_cycle(s, net, commands, done2)
		#print end
		ends.append(end)
	l = len(commands)
	n = 1
	for e in ends:
		n = n * e[0] / l
	print n * l

	return
	while True:
		n = n + 1
		if check_end(n, ends):
			print n
			break

if __name__ == "__main__":
	main()
