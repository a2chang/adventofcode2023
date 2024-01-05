#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_20_input.txt'
#test_input = 'test_input.text'
#test_input = 'test_input2.text'


class Module(object):
	FlipFlop = 'flip-flop'
	Conjunction = 'conjunction'
	Broadcast = 'broadcast'

	def __init__(self):
		self._name = '<none>'
		self._state = False
		self.dests = []
		self.low_count = 0

	def parse(self, spec_str):
		n, d = spec_str.split('>')
		d.strip(' -')
		self._name = n.strip(' -%&')
		#print self._name
		self.dests = [ i.strip() for i in d.strip(' ').split(',') ]
		#print self.dests
		return self._name

	def monitor_low(self, count):
		self.low_count = count

	def process(self, source, pulse, cycle):
		if not pulse and (self.low_count > 0):
			print('Module %s receive low on cycle %d' % (self._name, cycle))
			self.low_count = self.low_count - 1
		return pulse


class ModuleFF(Module):
	@staticmethod
	def is_spec(spec_str):
		return (len(spec_str) > 0) and (spec_str[0] == '%')

	def type(self):
		return Module.FlipFlop

	def process(self, source, pulse, cycle):
		if pulse:
			return None
		self._state = not self._state
		super(ModuleFF, self).process(source, pulse, cycle)
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

	def process(self, source, pulse, cycle):
		self.srcs[source] = pulse
		#print self.srcs
		super(ModuleC, self).process(source, pulse, cycle)
		return not all(self.srcs.values())


class ModuleB(Module):
	@staticmethod
	def is_spec(spec_str):
		return (len(spec_str) > 0) and (spec_str.startswith(Machine.broadcast))

	def type(self):
		return Module.Broadcast

	def process(self, source, pulse, cycle):
		super(ModuleB, self).process(source, pulse, cycle)
		return pulse


class Machine():
	broadcast = 'broadcaster'
	button = 'button'
	output = 'output'
	monitor_iterations = 5

	def __init__(self):
		self.pulses = {
			False: 0,
			True: 0,
		}
		self._modules = {}
		self.button_presses = 0
		self.halt = False
		self.monitor_list = []

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

	def monitor(self, module_name):
		self.monitor_list.append(module_name)
		mod = self._modules[module_name]
		mod.monitor_low(Machine.monitor_iterations)

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
			res = mod.process(signal[0], signal[2], self.button_presses)
			if res is not None:
				for d in mod.dests:
					self.queue_signal(signals, signal[1], d, res)
			
			if haltable and (len(self.monitor_list) > 0):
				remain = 0
				for module_name in self.monitor_list:
					mod = self._modules[module_name]
					remain = remain + mod.low_count
				if remain == 0:
					self.halt = True


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

	m.monitor('vg')
	m.monitor('nb')
	m.monitor('vc')
	m.monitor('ls')

	for i in range(1000):
		m.press_button()
	print m.score()

	while not m.halt:
		m.press_button(True)

	# Answer to part 2 is LCM of low cycles on: nb vc vg ls


if __name__ == "__main__":
	main()
