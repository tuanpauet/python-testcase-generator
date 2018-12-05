import rand
def replace_string (s):
	return s.replace ("\\n", "\n").replace ("\\'", "\'").replace ("\\\"", "\"").replace ("\\s", " ").replace ("\\\\", "\\")
def is_digit (c):
	return ord (c) >= ord ("0") and ord (c) <= ord ("9")
class var:
	_name = "default"
	_max = 9223372036854775807 # 2**63 - 1
	_min = -9223372036854775807 # -2**63 + 1
	_type = "int"
	_value = []
	_str_value = ""
	_prefix = ""
	_suffix = ""
	_only_one = False
	_first_str = ""
	_second_str = ""
	_multiply = ""
	_show_information = False # show information for variable before randomizing
	def to_string(self):
		if self._type == "int" or self._type == "float" or self._type == "char":
			return self._name + " in [" + str(self._min) + ", " + str(self._max) + "] prefix = '" + self._prefix + "' suffix = '" + self._suffix + "'"
		return self._name + " = '" + self._str_value + "' prefix = '" + self._prefix + "' suffix = '" + self._suffix + "'"
class vars:
	_var = {}
	def get(self, _var_name, _sys_argv):
		#print "_var_name = {}".format(_var_name)
		is_number = True
		for i in range (0, len(_var_name)):
			if not is_digit (_var_name[i]):
				is_number = False
		if is_number:
			_a = _sys_argv.split(",")
			#print _a
			if int(_var_name) <= len (_a) and len(_sys_argv) >= 1:
				return _a[int(_var_name) - 1]
			else:
				print "Cannot read variable ${} in _sys_argv {}. Aborting".format(_var_name, _sys_argv)
				exit()
		if (not _var_name in self._var):
			print "variable {} not found. Aborting".format (_var_name)
			exit()
		_v = self._var[_var_name]
		if _v._type == "string":
			if _v._show_information:
				print "{} = ".format(_v._name)
			return str(_v._str_value)
		if _v._type == "concatenate":
			first_str = ""
			second_str = ""
			if (_v._first_str[0] == "$"):
				first_str = str(self.get_string (_v._first_str[1], _sys_argv))
			else: 
				first_str = str(_v._first_str)
			if (_v._second_str[0] == "$"):
				second_str = str(self.get_string (_v._second_str[1], _sys_argv))
			else: 
				second_str = str(_v._second_str)
			if _v._show_information:
				print "{} = {} + {}".format(_v._name, _v._first_str, _v.second_str)
			return first_str + second_str
		if _v._type == "multiply":
			first_str = ""
			multiply = 0
			if (_v._multiply[0] == "$"):
				multiply = int(self.get(_v._multiply[1], _sys_argv))
			else:
				try:
					multiply = int(_v._multiply)
				except ValueError:
					print "Cannot cast multiply into int for variable {}. Aborting".format(_v._name)
					exit()
			if (_v._first_str[0] == "$" and _v._first_str[len(_first_str) - 1] == "$"):
				for i in range (0, multiply):
					first_str += str(self.get_string (_v._first_str[1], _sys_argv)) 
			else: 
				for i in range (0, multiply):
					first_str += str(_v._first_str)
			if _v._show_information:
				print "{} = {} * {}". format (_v._name, _v._first_str, _v.multiply) 
			return first_str
		if _v._type == "int":
			if str(_v._min)[0] == "$":
				_min = int(self.get(_v._min[1:], _sys_argv))
			else:
				_min = int (_v._min)
			if str(_v._max)[0] == "$":
				#print _v._max
				_max = int(self.get(_v._max[1:], _sys_argv))
			else:
				_max = int (_v._max)
			value = rand.rand_int(_min, _max)
			if _v._show_information:
				print "{} = {} in [{}, {}]". format (_v._name, value, _min, _max) 
			return value
		if _v._type == "float":
			if str(_v._min)[0] == "$":
				_min = float(self.get(_v._min[1:], _sys_argv))
			else:
				_min = float(_v._min)
			if str(_v._max)[0] == "$":
				_max = float(self.get(_v._max[1:], _sys_argv))
			else:
				_max = float(_v._max)
			value = rand.rand_float(_min, _max)
			if _v._show_information:
				print "{} = {} in [{}, {}]". format (_v._name, value, _min, _max) 
			return value;
		if _v._type == "char":
			if str(_v._min)[0] == "$":
				_min = chr(self.get(_v._min[1:], _sys_argv))
			else:
				_min = chr (_v._min)
			if str(_v._max)[0] == "$":
				_max = chr(self.get(_v._max[1:], _sys_argv))
			else:
				_max = chr (_v._max)
			value = rand.rand_chr(_min, _max)
			if _v._show_information:
				print "{} = {} in [{}, {}]". format (_v._name, value, _min, _max) 
		return ""
	def get_string(self, _var_name, _sys_argv):
		#print "_var_name = {}".format(_var_name)
		is_number = True
		for i in range (0, len(_var_name)):
			if not is_digit (_var_name[i]):
				is_number = False
		if len (_var_name) == 0: is_number = False
		if is_number:
			_a = _sys_argv.split(",")
			print len(_a)
			if int(_var_name) <= len (_a):
				return _a[int(_var_name) - 1]
			else:
				print "Cannot read variable ${} in _sys_argv {}. Aborting".format(_var_name, _sys_argv)
				exit()
		if (not _var_name in self._var):
			print "variable {} not found. Aborting".format (_var_name)
			exit()
		_v = self._var[_var_name]
		return _v._prefix + str(self.get(_var_name, _sys_argv)) + _v._suffix
def cast (s, t):
	if (s[0] == "$"): return s
	if t == "int": return int(s)
	if t == "float": return float(s)
	if t == "char": return s[:1]
	return s
def read_file (_path):
	# open the file
	_f = open (_path)

	#the _var result
	_var = {}

	for _l in _f:
		_l = _l.strip()
		d = False
		if (len (_l) <= 1 or _l[0] == '#'): continue
		for i in range (0, len (_l)):
			if _l[i] == ' ' and d: _l = _l[0:i] + "\\s" + _l[i+1:]
			if _l[i] == '"': d = not d  
		#print _l
		_a = _l.split (" ") 
		# _a[0] - variable name
		_name = _a[0]
		_var[_name] = var()
		_var[_name]._name = _name
		if _a[1] == "int": _var[_name]._type = "int"
		elif _a[1] == "float": _var[_name]._type = "float"
		elif _a[1] == "char": _var[_name]._type = "char"
		elif _a[1] == "string": _var[_name]._type = "string"
		elif _a[1] == "concatenate": 
			if (len(_a) >= 4):
				_var[_name]._type = "concatenate"
				_var[_name]._first_str = _a[2]
				_var[_name]._second_str = _a[3]
			else:
				print "Cannot read the _first_str and the _second_str for variable {}. Aborting".format(_name)
				exit()
		elif _a[1] == "multiply":
			if (len(_a) >= 4):
				_var[_name]._type = "multiply"
				_var[_name]._first_str = _a[2]
				_var[_name]._multiply = _a[3]
			else:
				print "Cannot read the _first_str and the _multiply for variable {}. Aborting".format(_name)
				exit()
		else:
			print "type {} of variable {} is not supported. Aborting".format(_a[1], _name)
			exit()
		for i in range (2, len(_a)):
			_s = _a[i][1:]
			_c = _a[i][0]
			if _c == "<": _var[_name]._max = cast (_s, _var[_name]._type)
			elif _c == ">": _var[_name]._min = cast (_s, _var[_name]._type)
			elif _c == "p": _var[_name]._prefix = replace_string(_s[1:-1])
			elif _c == "s": _var[_name]._suffix = replace_string(_s[1:-1])
			elif _c == "v": _var[_name]._str_value = replace_string(_s[1:-1])
			elif _c == "o": _var[_name]._only_one = True
			elif _c == "i": _var[_name]._show_information = True
			else: _var[_name]._value = replace_string(_a[i])
	_vars = vars()
	_vars._var = _var
	return _vars