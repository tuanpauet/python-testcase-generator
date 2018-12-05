import sys
import os
import random

#append the .make_test directory
sys.path.append(".make_test/")
import variable

#
_usage = "Usage: python make_test.py -n <number_of_tests> -i <test_input_path> -o <test_output_path> -x <executable_path> <parameter_test1> <parameter_test2> ..."
if len(sys.argv) == 1: 
	print _usage
	exit()

print "Reading configuration from make_test.conf"
_vars = variable.read_file ("make_test.conf")
#for k, v in _vars._var.iteritems():
#	print "{}".format(v.to_string())

_test_input_path = "$i$/input"
_test_output_path = "$i$/output"
_executable_path = "none"

# check the _var
# test_input_path
if not "_test_input_path" in _vars._var: print "_test_input_path is not set in variable.conf"
else: _test_input_path = _vars._var["_test_input_path"]._value
# test_output_path
if not "_test_output_path" in _vars._var:	print "_test_output_path is not set in variable.conf"
else: _test_output_path = _vars._var["_test_output_path"]._value
# executable_path
if not "_executable_path" in _vars._var: print "_executable_path is not set in variable.conf"
else: _executable_path = _vars._var["_executable_path"]._value

_number_of_tests = 0
_parameter = []
def get_parameter (i):
	if (i >= len(_parameter)): return ""
	else: return _parameter[i].strip()
i = 1
while i < len(sys.argv):
	if (sys.argv[i] == "-n"):
		if (i + 1 < len(sys.argv)):
			_number_of_tests = int(sys.argv[i + 1])
			i = i + 1
		else: 
			print _usage
	elif sys.argv[i] == "-i":
		if (i + 1 < len(sys.argv)):
			_test_input_path = sys.argv[i + 1]
			i = i + 1
		else:
			print _usage
	elif sys.argv[i] == "-o":
		if (i + 1 < len(sys.argv)):
			_test_output_path = sys.argv[i + 1]
			i = i + 1
		else:
			print _usage
	elif sys.argv[i] == "-x":
		if (i + 1 < len(sys.argv)):
			_test_input_path = sys.argv[i + 1]
			i = i + 1
		else:
			print _usage
	else:
		_parameter.append (sys.argv[i])
	i = i + 1
_number_of_tests = max(_number_of_tests, len(_parameter))

print "Running make_test with configuration: "
print " - _number_of_tests = {}".format (_number_of_tests)
print " - _test_input_path = {}".format (_test_input_path)
print " - _test_output_path = {}".format (_test_output_path)
print " - _executable_path = {}".format (_executable_path)

# Generate values and write to files
for i in range (0, _number_of_tests):
	#
	print ""
	_input_path = _test_input_path.replace ("$_i", str(i + 1))
	_output_path = _test_output_path.replace ("$_i", str(i + 1))
	os.system("mkdir -p " + os.path.dirname (_input_path))
	print "Generating test {} and writing to file {}".format(i + 1, _input_path)
	f = open (_input_path, "w")
	f.write (str(_vars.get("output", get_parameter(i))))
	f.close()
	command = "{} < {} > {}".format(_executable_path, _input_path, _output_path)
	print "Running solution for test {} command '{}'".format (i + 1, command)
	os.system(command)
	
print "Done."