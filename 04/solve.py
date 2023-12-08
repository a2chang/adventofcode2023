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

	matches = 0
	while True:
		if w == p:
			matches = matches + 1
		if p > w:
			if len(picks) == 0:
				break
			p = picks.pop()
		else:
			if len(winners) == 0:
				break
			w = winners.pop()
	return matches


def get_points(matches):
	if matches > 0:
		return 2**(matches-1)
	return 0


def _is_winnings_complete(winnings, start=0, end=0):
	if end == 0:
		end = len(winnings)
	for v in winnings[start:end]:
		if v is None:
			return False
	return True


def _fill_winnings(winnings, size, wins, round):
	# Iterate from the end
	for i in reversed(range(size)):
		if winnings[i] is None and wins[i] == round:
			if _is_winnings_complete(winnings, i+1, i+1+round):
				winnings[i] = sum(winnings[i+1:i+1+round]) + 1


def get_winnings(wins):
	size = len(wins)
	winnings = [ None ] * size

	# Highest number of prizes won in a single tickets
	max_win = max(wins)

	# Each ticket that does not win any more is worth a single ticket
	for i in reversed(range(size)):
		if wins[i] == 0:
			winnings[i] = 1

	while not _is_winnings_complete(winnings):
		# Iterate by prizes
		for round in range(1, max_win+1):
			_fill_winnings(winnings, size, wins, round)

	print sum(winnings)


def main():
	lines = read(test_input)

	wins = []

	# Part 1
	sum = 0
	for line in lines:
		line = line.strip('\n')
		matches = parse_line(line)
		wins.append(matches)
		sum = sum + get_points(matches)
	print sum

	# Part 2
	size = len(wins)
	tickets = get_winnings(wins)
	tickets = [ 1 ] * size


if __name__ == "__main__":
	main()
