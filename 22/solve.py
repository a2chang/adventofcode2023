#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_22_input.txt'
#test_input = 'test_input.text'


class Brick():
	_lastid = 1

	@staticmethod
	def range_overlap(a0, a1, b0, b1):
		cond = not ((a0 > b1) or (b0 > a1))
		#print('%d-%d / %d-%d / %d' % (a0, a1, b0, b1, cond))
		return cond

	def __init__(self):
		# Character of node
		self.id = Brick._lastid
		Brick._lastid = Brick._lastid + 1
		self.drop = 0
		self.touchd = []
		self.touchu = []

	def load(self, line):
		s,e = line.split('~')
		x0, y0, z0 = s.split(',')
		x1, y1, z1 = e.split(',')
		x0 = eval(x0)
		x1 = eval(x1)
		y0 = eval(y0)
		y1 = eval(y1)
		z0 = eval(z0)
		z1 = eval(z1)
		if (x0 < x1):
			self.x0 = x0
			self.x1 = x1
		else:
			self.x0 = x1
			self.x1 = x0
		if (y0 < y1):
			self.y0 = y0
			self.y1 = y1
		else:
			self.y0 = y1
			self.y1 = y0
		if (z0 < z1):
			self.z0 = z0
			self.z1 = z1
		else:
			self.z0 = z1
			self.z1 = z0

	def set_drop(self, dz):
		self.drop = dz

	def set_bottom(self, z1):
		self.drop = self.z0 - z1 - 1

	def get_top(self):
		return self.z1 - self.drop

	def get_bottom(self):
		return self.z0 - self.drop - 1

	def overlap(self, b):
		#print('%d %d overlap test' % (self.id, b.id))
		if not Brick.range_overlap(self.x0, self.x1, b.x0, b.x1):
			return False
		if not Brick.range_overlap(self.y0, self.y1, b.y0, b.y1):
			return False
		#print('%d %d overlap' % (self.id, b.id))
		return True

	def debug(self):
		print('%3d   (%d, %d, %d) - (%s, %d, %d)  %d %s %s' %
				(self.id, self.x0, self.y0, self.z0, self.x1, self.y1, self.z1,
				self.drop, self.touchd, self.touchu))


class Tetris():
	def __init__(self):
		self.bricks = {}
		self.zmap = {}

	@staticmethod
	def add_zorder(zmap, brick):
		zlayer = zmap.get(brick.z0, None)
		if zlayer is None:
			zmap[brick.z0] = []
			zlayer = zmap.get(brick.z0, None)
		if brick.id not in zlayer:
			zlayer.append(brick.id)

	def load(self, lines):
		for line in lines:
			if '~' in line:
				brick = Brick()
				brick.load(line)
				self.bricks[brick.id] = brick

				Tetris.add_zorder(self.zmap, brick)

				#zlayer = self.zmap.get(brick.z0, None)
				#if zlayer is None:
				#	self.zmap[brick.z0] = []
				#	zlayer = self.zmap.get(brick.z0, None)
				#zlayer.append(brick.id)

	def apply_gravity(self):
		zeds = self.zmap.keys()
		zeds.sort()

		for i in range(len(zeds)):
			z = zeds[i]
			#print('i=%d / %d' % (i, z))
			for brickid in self.zmap[z]:
				#print brickid
				brick = self.bricks[brickid]
				floor = 0
				floor_bricks = []
				for j in range(i):
					zsub = zeds[j]
					#print('j=%d / %d' % (j, zsub))
					for bsubid in self.zmap[zsub]:
						bsub = self.bricks[bsubid]
						if brick.overlap(bsub):
							bsubtop = bsub.get_top()
							#print('bsubtop=%d / floor=%d' % (bsubtop, floor))
							if bsubtop > floor:
								floor = bsubtop
								floor_bricks = []
							if bsubtop == floor:
								floor_bricks.append(bsub.id)
				brick.set_bottom(floor)
				for bsubid in floor_bricks:
					bsub = self.bricks[bsubid]
					brick.touchd.append(bsub.id)
					bsub.touchu.append(brick.id)


	def find_non_structural(self):
		results = []
		for b in self.bricks:
			stable = True
			brick = self.bricks[b]
			for topper in brick.touchu:
				tbrick = self.bricks[topper]
				if len(tbrick.touchd) <= 1:
					stable = False
			if stable:
				results.append(b)
		return results


	def _get_above(self, brickid):
		s = set()
		brick = self.bricks[brickid]
		for topper in brick.touchu:
			s.add(topper)
			s = s.union(self._get_above(topper))
		return s
			

	def find_structural(self):
		zapped_sets = {}
		for b in self.bricks:
			above = self._get_above(b)
			tower = {}
			for bup in above:
				Tetris.add_zorder(tower, self.bricks[bup])

			zapped = { b }

			zeds = tower.keys()
			zeds.sort()

			for z in zeds:
				for zbid in tower[z]:
					zblock = self.bricks[zbid]
					if set(zblock.touchd) <= zapped:
						zapped.add(zbid)

			zapped.remove(b)
			if len(zapped) > 0:
				zapped_sets[b] = zapped

		return zapped_sets



	def debug(self):
		for b in self.bricks:
			self.bricks[b].debug()
		for z in self.zmap:
			print('%d - %s' % (z, self.zmap[z]))


def part2score(structures):
	score = 0
	for s in structures:
		score = score + len(structures[s])
	return score


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


def main():
	lines = read(test_input)
	tetris = Tetris()
	tetris.load(lines)
	#tetris.debug()
	tetris.apply_gravity()
	#tetris.debug()
	disintegrable = tetris.find_non_structural()
	print len(disintegrable)

	structures = tetris.find_structural()
	count = part2score(structures)
	print count


if __name__ == "__main__":
	main()
