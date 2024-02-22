#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_24_input.txt'
area_min = 200000000000000
area_max = 400000000000000

def use_test():
	global test_input
	global area_min
	global area_max
	test_input = 'test_input.text'
	area_min = 7
	area_max = 27



class Vector():
	@staticmethod
	def from_str(vstr):
		x, y, z = vstr.split(',')
		return [eval(x), eval(y), eval(z)]

	@staticmethod
	def from_ints(x, y, z):
		return [x, y, z]

	@staticmethod
	def mult_scalar(v, c):
		return [ vv*c if vv is not None else None for vv in v ]

	@staticmethod
	def add(v1, v2):
		print('%s + %s' % (v1, v2))
		ret = []
		for i in range(len(v1)):
			if v1[i] is None or v2[i] is None:
				ret.append(None)
			else:
				ret.append(v1[i] + v2[i])
		return ret


class Hail():
	last_id = 1

	@staticmethod
	def is_hail(line):
		return '@' in line

	def __init__(self, line):
		self.id = Hail.last_id
		Hail.last_id = Hail.last_id + 1

		pstr, vstr = line.split('@')
		self.p = Vector.from_str(pstr)
		self.v = Vector.from_str(vstr)
		self.tmin = None
		self.tmax = None

	def bound(self, bmin, bmax, clip):
		mins = []
		maxs = []
		for i in range(len(self.p)):
			p = self.p[i]
			v = self.v[i]
			b0 = bmin[i]
			b1 = bmax[i]
			if b0 is not None and b1 is not None:
				t0 = (b0 - p) / v
				t1 = (b1 - p) / v
				if t0 < t1:
					mins.append(t0)
					maxs.append(t1)
				else:
					mins.append(t1)
					maxs.append(t0)
		self.tmin = max(mins)
		if clip and self.tmin < 0:
			self.tmin = 0
		self.tmax = min(maxs)

	def debug(self):
		print('%d: %s @ %s / %s:%s' % (self.id, self.p, self.v,
								'-' if self.tmin is None else self.tmin,
								'-' if self.tmax is None else self.tmax))

class Area():
	def __init__(self):
		self._stones = []


	def load(self, lines):
		for line in lines:
			if Hail.is_hail(line):
				h = Hail(line)
				self._stones.append(h)

	def bound(self, clip=True, useZ=False):
		bmin = [ area_min, area_min, area_min if useZ else None ]
		bmax = [ area_max, area_max, area_max if useZ else None ]
		for h in self._stones:
			h.bound(bmin, bmax, clip)


	def _xy_collision(self, h0, h1):
		p0x = float(h0.p[0])
		p0y = float(h0.p[1])
		v0x = float(h0.v[0])
		v0y = float(h0.v[1])
		p1x = float(h1.p[0])
		p1y = float(h1.p[1])
		v1x = float(h1.v[0])
		v1y = float(h1.v[1])

		if v1x == 0:
			return [ None, None ]
		if v1y == 0:
			return [ None, None ]
		denom = (v0x/v1x - v0y/v1y)
		if denom == 0:
			return [ None, None ]
		t0 = ( (p0y-p1y)/v1y - (p0x-p1x)/v1x ) / denom
		t1 = (p0x - p1x + t0*v0x) / v1x
		return [t0, t1]


	def xy_collision_count(self):
		count = 0
		for i in range(len(self._stones)):
			h0 = self._stones[i]
			for j in range(i+1, len(self._stones)):
				h1 = self._stones[j]
				t = self._xy_collision(h0, h1)
				if t[0] is not None and t[1] is not None and t[0] >= h0.tmin and t[0] <= h0.tmax and t[1] >= h1.tmin and t[1] <= h1.tmax:
					count = count + 1
					#print('%d/%d collide' % (h0.id, h1.id))
		return count


	def test(self):
		for h in self._stones:
			h.debug()
		return
		h = self._stones[0]
		h.debug()
		print Vector.mult_scalar(h.p, 2)
		v1 = Vector.from_ints(1, 2, None)
		print Vector.add(h.p, v1)


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


def main():
	#use_test()
	lines = read(test_input)
	area = Area()
	area.load(lines)
	area.bound(True, False)
	#area.bound(True)
	#area.test()
	print area.xy_collision_count()


if __name__ == "__main__":
	main()
