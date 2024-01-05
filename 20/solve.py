#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_20_input.txt'
#test_input = 'test_input.text'
#test_input = 'test_input2.text'


class Module(object):
	FlipFlop = 'flip-flop'
	Conjunction = 'conjunction'
	Broadcast = 'broadcast'
	RX = 'rx'

	def __init__(self):
		self._name = '<none>'
		self._state = False
		self.dests = []

	def parse(self, spec_str):
		n, d = spec_str.split('>')
		d.strip(' -')
		self._name = n.strip(' -%&')
		#print self._name
		self.dests = [ i.strip() for i in d.strip(' ').split(',') ]
		#print self.dests
		return self._name

	def process(self, source, pulse):
		return pulse


class ModuleFF(Module):
	@staticmethod
	def is_spec(spec_str):
		return (len(spec_str) > 0) and (spec_str[0] == '%')

	def type(self):
		return Module.FlipFlop

	def process(self, source, pulse):
		if pulse:
			return None
		self._state = not self._state
		return self._state


class ModuleC(Module):
	def __init__(self):
		self.srcs = {}
		Module.__init__(self)

	@staticmethod
	def is_spec(spec_str):
		return (len(spec_str) > 0) and (spec_str[0] == '&')

	def type(self):
		return Module.Conjunction

	def add_src(self, source):
		self.srcs[source] = False

	def process(self, source, pulse):
		self.srcs[source] = pulse
		#print self.srcs
		return not all(self.srcs.values())


class ModuleB(Module):
	@staticmethod
	def is_spec(spec_str):
		return (len(spec_str) > 0) and (spec_str.startswith(Machine.broadcast))

	def type(self):
		return Module.Broadcast

	def process(self, source, pulse):
		return pulse


class ModuleRX(Module):
	def type(self):
		return Module.RX

	def process(self, source, pulse):
		if pulse is False:
			return None
		return pulse


class Machine():
	broadcast = 'broadcaster'
	button = 'button'
	output = 'output'

	def __init__(self):
		self.pulses = {
			False: 0,
			True: 0,
		}
		self._modules = {}
		self.button_presses = 0
		self.halt = False


	def load(self, lines):
		for line in lines:
			if ModuleFF.is_spec(line):
				m = ModuleFF()
			elif ModuleC.is_spec(line):
				m = ModuleC()
			elif ModuleB.is_spec(line):
				m = ModuleB()
			mod = m.parse(line)
			self._modules[mod] = m

		for n in self._modules:
			for d in self._modules[n].dests:
				dmod = self._modules.get(d, None)
				if dmod is not None and (dmod.type() == Module.Conjunction):
					dmod.add_src(n)


	def _pretty(self, signal):
		pulse = 'high' if signal[2] else 'low'
		print('%s -%s-> %s' % (signal[0], pulse, signal[1]))


	def queue_signal(self, signals, src, dest, pulse):
		self.pulses[pulse] = self.pulses[pulse] + 1
		signals.append( [ src, dest, pulse ] )


	def press_button(self, haltable=False):
		self.button_presses = self.button_presses + 1
		# src, dest, pulse
		#signals = [ [ Machine.button, Machine.broadcast, False ] ]
		signals = []
		self.queue_signal(signals, Machine.button, Machine.broadcast, False)
		while len(signals) > 0:
			signal = signals.pop(0)
			if signal[1] == Machine.output:
				#print 'Output: %s' % signal
				#self._pretty(signal)
				continue
			#self._pretty(signal)
			mod = self._modules.get(signal[1])
			if mod is None:
				continue
			res = mod.process(signal[0], signal[2])
			if res is not None:
				for d in mod.dests:
					self.queue_signal(signals, signal[1], d, res)
			elif mod.type() == Module.RX:
				print('Halt at %d presses' % self.button_presses)
				self.halt = True
				if haltable:
					return

	def prune(self, needed):
		last = ''
		while str(needed) != last:
			last = str(needed)
			print needed
			for need in set(needed):
				# Find all modules that signal need
				for n in self._modules:
					if need in self._modules[n].dests:
						needed.add(n)

		for n in self._modules.keys():
			if n not in needed:
				print('Pruned %s' % n)
				self._modules.pop(n)
			else:
				print('Kept %s' % n)


	def score(self):
		return self.pulses[True] * self.pulses[False]

	def test(self):
		pass


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


def main():
	lines = read(test_input)
	m = Machine()
	m.load(lines)
	#for i in range(1000):
	for i in range(1000):
		m.press_button()
	print m.score()

	m.prune( { Module.RX } )
	while not m.halt:
		m.press_button()


if __name__ == "__main__":
	main()
