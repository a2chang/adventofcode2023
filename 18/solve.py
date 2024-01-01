#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_18_input.txt'
#test_input = 'test_input.text'


class Map():

	def __init__(self):
		self._digplan = []
		self._vsegments = []	# [y0, y1, x]
		self._hsegments = []	# [y, x0, x1, monotone]
		self._yrows = {''}



	def parse1(self, digplan):
		for r in digplan:
			dir, dist, col = r.split()
			self._digplan.append( (dir, eval(dist), col) )

	def parse2(self, digplan):
		for r in digplan:
			_, _, col = r.split()
			cmd = col.strip('()').replace('#','0x')
			dir = None
			if cmd[-1] == '0':
				dir = 'R'
			elif cmd[-1] == '1':
				dir = 'D'
			elif cmd[-1] == '2':
				dir = 'L'
			elif cmd[-1] == '3':
				dir = 'U'
			self._digplan.append( (dir, eval(cmd[:-1]), col) )


	def build_segments(self):
		x = 0
		y = 0
		last = 'S'

		for (dir, dist, _) in self._digplan:
			if dir == 'L':
				self._yrows.add(y)
				self._hsegments.append( [ y, x-dist, x, None ] )
				x = x - dist
			elif dir == 'R':
				self._yrows.add(y)
				self._hsegments.append( [ y, x, x+dist, None ] )
				x = x + dist
			elif dir == 'U':
				self._vsegments.append( [ y-dist, y, x ] )
				y = y - dist
				if len(self._hsegments) > 0:
					self._hsegments[-1][-1] = (last == dir)
				last = dir
			elif dir == 'D':
				self._vsegments.append( [ y, y+dist, x ] )
				y = y + dist
				if len(self._hsegments) > 0:
					self._hsegments[-1][-1] = (last == dir)
				last = dir

		dir, _, _ =  self._digplan[-1]
		if dir in 'UD':
			dir0, _, _ =  self._digplan[0]
			if dir0 not in 'UD':
				dir0, _, _ =  self._digplan[1]
			self._hsegments[0][-1] = (dir0 == dir)
		else:
			self._hsegments[-1][-1] = (last == dir)

		#print self._vsegments
		#print self._hsegments


	def get_row_area(self, y):
		segs = {}
		for vs in self._vsegments:
			if (vs[0] < y) and (y < vs[1]):
				segs[vs[2]] = [ vs[2], True ]
		for hs in self._hsegments:
			if hs[0] == y:
				segs[hs[1]] = [ hs[2], hs[3] ]
		#print segs

		area = 0
		fill = False
		lastx = None

		keys = segs.keys()
		keys.sort()
		for x in keys:
			if fill:
				if segs[x][1]:
					area = area + segs[x][0] - lastx + 1
					#print('A: +%d: %d' % (segs[x][0] - lastx + 1, area))
					fill = False
			else:
				if not segs[x][1]:
					area = area + segs[x][0] - x + 1
					#print('B: +%d: %d' % (segs[x][0] - x + 1, area))
				else:
					lastx = x
					fill = True

		#print('Row %d - %d' % (y, area))
		return area


	def get_area(self):
		area = 0
		rows = list(self._yrows)[1:]
		rows.sort()

		y0 = rows[0]
		area = area + self.get_row_area(y0)

		for i in range(1, len(rows)):
			y = rows[i]
			a = self.get_row_area(y0+1)
			area = area + (y - y0 - 1) * a

			a = self.get_row_area(y)
			area = area + a

			y0 = y

		return area


	def debug(self):
		for (dir, dist, _) in self._digplan:
			print('%s %d' % (dir, dist) )



def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


def main():
	lines = read(test_input)
	m = Map()
	m.parse1(lines)
	m.build_segments()
	area = m.get_area()
	print area

	m = Map()
	m.parse2(lines)
	#m.debug()
	m.build_segments()
	area = m.get_area()
	print area


if __name__ == "__main__":
	main()
