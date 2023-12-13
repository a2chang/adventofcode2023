#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_7_input.txt'
#test_input = 'test_input.text'


class Hand():

	# Rank string 'hccccc'
	# - h is character representing hand:
	#	- 9 for 5 of a kind
	#	- 8 for 4 of a kind
	#	- 7 for full house
	#	- 6 for 3 of a kind
	#	- 5 for two pair
	#	- 4 for one pair
	#	- 3 for high card
	# - ccccc is the cards with the following mapping:
	#	- c for T
	#	- d for J
	#	- e for Q
	#	- f for K
	#	- g for A

	def __init__(self, cards, bid):
		self._cards = cards
		self._bid = bid
		self._rankstr = None

	def get_rankstr(self):
		# First map face cards to a sortable character
		self._rankstr = self._cards
		self._rankstr = self._rankstr.replace('T', 'c')
		self._rankstr = self._rankstr.replace('J', 'd')
		self._rankstr = self._rankstr.replace('Q', 'e')
		self._rankstr = self._rankstr.replace('K', 'f')
		self._rankstr = self._rankstr.replace('A', 'g')

		# Now determine hand type
		m = {}
		for i in list(self._cards):
			m[i] = m.get(i, 0) + 1
		histo = m.values()
		histo.sort(reverse = True)

		if histo[0] == 5:
			self._rankstr = '9' + self._rankstr
		elif histo[0] == 4:
			self._rankstr = '8' + self._rankstr
		elif histo[0] == 3:
			if histo[1] == 2:
				self._rankstr = '7' + self._rankstr
			else:
				self._rankstr = '6' + self._rankstr
		elif histo[0] == 2:
			if histo[1] == 2:
				self._rankstr = '5' + self._rankstr
			else:
				self._rankstr = '4' + self._rankstr
		else:
			self._rankstr = '3' + self._rankstr

		return self._rankstr


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	return lines


def parse_line(line):
	print line
	cards, bid = line.split()
	hand = Hand(cards, bid)
	return hand.get_rankstr(), int(bid)


def parse(lines):
	hands = {}
	for line in lines:
		line = line.strip('\n')
		hand, bid = parse_line(line)
		hands[hand] = bid

	winnings = 0
	rank = 1
	keys = [ k for k in hands.iterkeys() ]
	keys.sort()
	for k in keys:
		#print '%s - %d' % (k, hands[k])
		winnings = winnings + rank * hands[k]
		rank = rank + 1
	print winnings


def main():
	lines = read(test_input)

	# Part 1
	parse(lines)

	# Part 2


if __name__ == "__main__":
	main()
