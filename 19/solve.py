#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_19_input.txt'
#test_input = 'test_input.text'


class State():
	start = 'in'

	def __init__(self):
		# Character of node
		self.name = '<none>'
		self._transitions = []

	@staticmethod
	def is_state(rule):
		return (len(rule) > 0) and rule[0].isalpha()

	@staticmethod
	def is_good(state):
		return (state == 'A')

	@staticmethod
	def is_bad(state):
		return (state == 'R')

	def _parse_transition(self, t):
		if t.find(':') == -1:
			return [ None, None, None, t ]

		cond, state = t.split(':')
		var = cond[0]
		comp = cond[1]
		value = eval(cond[2:])
		return [ var, comp, value, state ]

	def parse(self, rule):
		self.name, rest = rule.split('{')
		rest = rest.strip('}')
		transits = rest.split(',')

		for t in transits:
			self._transitions.append(self._parse_transition(t))

	def step(self, part):
		for t in self._transitions:
			if t[0] is None:
				return t[3]

			v = part.vars[t[0]]
			if t[1] == '>':
				if v > t[2]:
					return t[3]
			elif t[1] == '<':
				if v < t[2]:
					return t[3]
		return None

	def debug(self):
		print self.name
		print self._transitions


class Part():
	def __init__(self):
		self.vars = {}

	@staticmethod
	def is_part(rule):
		return (len(rule) > 0) and (rule[0] == '{')

	def parse(self, rule):
		rule = rule.strip('{}')
		for a in rule.split(','):
			var = a[0]
			value = eval(a[2:])
			self.vars[var] = value

	def score(self):
		return sum(self.vars.values())

	def debug(self):
		print self.vars


class Machine():

	def __init__(self):
		self._states = {}
		self._parts = []

	def load(self, lines):
		for line in lines:
			if State.is_state(line):
				state = State()
				state.parse(line)
				#state.debug()
				self._states[state.name] = state
			if Part.is_part(line):
				part = Part()
				part.parse(line)
				#part.debug()
				self._parts.append(part)

	def run_part(self, part):
		state = State.start
		while not State.is_good(state) and not State.is_bad(state):
			s = self._states.get(state, None)
			state = s.step(part)
		return State.is_good(state)


	def run_parts(self):
		total = 0
		for p in self._parts:
			ret = self.run_part(p)
			if ret:
				total = total + p.score()
		print total


	def test(self):
		print self._states
		print self._parts


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


def main():
	lines = read(test_input)
	m = Machine()
	m.load(lines)
	m.run_parts()
	#m.test()


if __name__ == "__main__":
	main()
