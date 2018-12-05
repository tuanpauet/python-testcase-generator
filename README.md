# python-testcase-generator
A simple testcase generator script written in Python 

I wrote this script when I had to generate testcases for a competitive programming problem. First time to write a script in Python, and I have no idea how to make this useful for the world. Feel free to contribute to the project

### How this works
* **Step 1:** The script reads the configuration from `make_test.conf` and find the variable `output`, `_test_input_path`, `_test_output_path` and `_executable_path`
* **Step 2:** Generate multiple output strings in the form of `output` variable, and write them to corresponding test input file (in the form of `_test_input_path`)
* **Step 3:** Execute the `_executable_path` with stdin redirected to test_input_file and stdout redirected to a test output file (in the form of `_test_output_path`)

### The configuration file 
- Every line of the configuration is considered as a variable except lines start with character "#"
- Every variable has to be defined in the form:
`<variable_name> <variable_type> <parameter_1> <parameter_2> ... `
          
### Variable
##### There are many types of variable supported (updated regularly)
- int - An integer with parameter < > <= >= != (some may not be available yet)
- float - A float with parameter < > <= >= != (some may not be available yet)
- char - A character with parameter < > <= >= != (some may not be available yet)
- string - A string with paraveter value (v) (no random supported)
- concatenate - A string which is made from concatenating two other strings
- multiply - A string which is made from multiplying other strings
##### Use variable as number in parameter
* To use variable in parameter we put the "$" character before the variable name. For example, we define the value of variable n as the max of variable i, we can use `i int <$n`
* To use value passed in the command line parameter, we put the "$" character before a number. For example, the command line of the script `python make_test.py 5,6,7` the `$1 = 5`, `$2 = 6`, and `$3 = 7`
* In the `_test_input_path` or `_test_output_path` variable, `$_i` results the counter of testcases generator loop
##### Parameters supported (updated regularly)
- <$n: define the max of the variable as $n
- \>5: define the min of the variable as 5
- \>a <d: define the min and the max of character-typed variable
- v"str ing": define the value for string variable
- o: feature comming soon
- i: show value of the variable everytime it is generated
- p"prefix": set prefix for the variable which is put before the generated value
- s"suffix": set suffix for the variable which is put after the generated value
##### Special characters in string
- \n: newline
- \\\': single quote
- \\\": double quote
- \\\\: backslash
### Commandline parameter
`python make_test.py -n <number_of_test> -i <test_input_path> -o <test_output_path> -x <executable_path> <parameters>`
* `-n`: Set the number of tests should be generated (**required**)
* `-i`: Set the test_input_path. If `-i` is not defined the the _test_input_path will be defined by the configuration file
* `-o`: Set the test_output_path. If `-o` is not defined the the _test_output_path will be defined by the configuration file
* `-x`: Set the executable_path. If `-x` is not defined the the _executable_path will be defined by the configuration file
* `parameters`: The list of parameter for each test case. For example, the parameter string is `1,2,3 4,5,6 7,8,9` then `1,2,3` will be used for testcase number 1, `4,5,6` will be used for testcase number 2, and `7,8,9` will be used for testcase number 3. See the **Use variable as number in parameter** for more details
* **If the number of parameters is smaller the n the number of testcases, then the last testcases will use "" as parameter string**
