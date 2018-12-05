import random
def rand (_min, _max): #inclusive
	_range = _max - _min
	r = random.random() #0.0 -> 1.0
	r = r * _range #0.0 -> _max - _min
	r = r + _min #_min -> _max
	if (r > _max): return _max
	if (r < _min): return _min
	return r
def _rand_int(_min, _max): #inclusive
	if (_max < _min):
		print "Cannot make a random in [{}, {}]. Aborting".format(_min, _max)
		exit()
	_range = _max - _min
	_random = random.random() * 1000000007 #0.0 -> 1.0 * 1000000007
	r = int (_random) % (_range + 1) # 0 -> _max - _min
	r = r + _min #_min -> _max
	if (r < _min): return _min
	if (r > _max): return _max
	return r
def _rand_float (_min, _max): #inclusive
	if (_max < _min):
		print "Cannot make a random in [{}, {}]. Aborting".format(_min, _max)
		exit()
	_range = _max - _min
	_random = random.random() #0.0 -> 1.0
	r = _random % _range # 0 -> _max - _min
	r = r + _min #_min -> _max
	if (r < _min): return _min
	if (r > _max): return _max
	return r
def _rand_char (_min, _max): #inclusive
	return ord(_rand_int (ord(_min), ord(_max)))

def rand_int (_min, _max): #exclusive
	return _rand_int(_min + 1, _max - 1)
def rand_float (_min, _max): #exclusive
	_range = _max - _min
	_random = random.random() #0.0 -> 1.0
	r = _random % _range # 0 -> _max - _min
	r = r + _min #_min -> _max
	if (r <= _min): return _min + 0.000000001
	if (r > _max): return _max - 0.000000001
	return r
def rand_chr (_min, _max): #exclusive
	return ord(rand_int (ord(_min), ord(_max)))