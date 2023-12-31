#!/usr/bin/python


test_input = 'adventofcode.com_2023_day_12_input.txt'
#test_input = 'test_input.text'


def read(filename):
	file1 = open(filename, 'r')
	lines = file1.readlines()
	lines = [ line.strip('\n') for line in lines ]
	return lines


# . is operational
# # is damaged
def get_signature(pattern):
	state = None
	count = 0
	sig = []
	for c in pattern:
		if c != '.':
			count = count + 1
		else:
			if state != '.':
				if count > 0:
					sig.append(count)
				count = 0
		state = c
	if count > 0:
		sig.append(count)
	return sig


def get_wcs(pattern):
	# Find wildcards
	wcs = []
	i = 0
	while i < len(pattern):
		if pattern[i] == '?':
			wcs.append(i)
		i = i + 1
	return wcs


def get_iteration(array, wcs, iter):
	for i in range(len(wcs)):
		array[wcs[i]] = '#' if (iter & (1 << i)) else '.'
	s = ''.join(array)
	#print s
	return s


def iterate(pattern, wcs, signature):
	sig_order = sum(signature)
	pat_order = len(pattern.replace('?', '').replace('.', ''))
	bits_needed = sig_order - pat_order

	#print '%s ------ %d %d %d' % (signature, sig_order, pat_order, bits_needed)
	matches = 0
	array = list(pattern)
	for i in range(2**len(wcs)):
		if bin(i).count('1') != bits_needed:
			continue
		pat = get_iteration(array, wcs, i)
		sig = get_signature(pat)
		#print sig
		if sig == signature:
			matches = matches + 1
	return matches


def gobble(pat, sig, searched):
	#print ('gobble %s %s' % (pat, sig))
	pat = pat.lstrip('.')

	cache_sigs = searched.get(pat, None)
	if cache_sigs is not None:
		count = cache_sigs.get(str(sig), None)
		if count is not None:
			return count

	# End of our groups
	if sig == []:
		#print ('end sig')
		if pat.count('#') == 0:
			return 1
		else:
			return 0

	# Are there enough characters left for the groups?
	if len(pat) < (sum(sig) + len(sig) - 1):
		#print ('too short')
		return 0
	need = sig[0]
	if len(pat) < need:
		return 0

	count = 0
	if pat[0:need].count('.') == 0:
		if pat[need] != '#':
			count = count + gobble(pat[need+1:], sig[1:], searched)

	if pat[0] != '#':
		count = count + gobble(pat[1:], sig, searched)

	if cache_sigs is None:
		cache_sigs = {}
		searched[pat] = cache_sigs
	cache_sigs[str(sig)] = count

	return count


def parse(line, fudge = 1):
	pattern, s = line.split()

	pattern = '?'.join( [ pattern ] * fudge )
	signature = s.split(',')
	signature = [ eval(s) for s in signature ] * fudge
	#print pattern
	#print signature

	return gobble(pattern + '.', signature, {})


def main():
	lines = read(test_input)

	# Part 1
	sum = 0
	for line in lines:
		sum = sum + parse(line)
	print sum

	# Part 2
	sum = 0
	for line in lines:
		sum = sum + parse(line, 5)
	print sum


if __name__ == "__main__":
	main()
