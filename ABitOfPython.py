# Welcome to A Bit of Python.
# These are single line comments.
# They're sort of like // Comments in C++

'''Multiline comments are written with triple-
single-quotes (like these ->)'''

"""Or triple-double-quotes. Technically, these are just
multiline strings, but if you don't assign them into
anything they're basically just comments."""

# Assignment may look funny to people coming from statically typed languages
# Variables aren't typed - the objects they point to ARE. You can reassign
# objects of different types into the same variable name, but you can't
# use objects as types other than what they are
a = 10
b = 23
a = "hello"

# So a + b would not work here. Thus, Python is a dynamically-typed and
# strongly-typed language

# Speaking of types, we have integers (of arbitrary precision):
x = 0
y = 232
z = 1238372716236327182932737283922837574728293

# You can do all the usual operations on them:
x = y * 2
y = z + 4 * 10 - (x - y)

# Augmented assignment (like in C and C++) is allowed:
x += y
z *= 10

# We have floats:
pi = 3.141
big = 2.93e24

# We also have strings:
s1 = "hello"
s2 = ' world!'
s3 = s1 + s2

# There's no difference between single and double-quoted strings.
# They just make it easier to embed quotes:
sq = 'Joe said, "This Python primer is terrible."'
dq = "Joe can't read good."

# You've already seen multiline strings. Here is one that's NOT a comment:
multiline = """Sometimes you're writing something, and it takes way longer
than one line, especially if you're given to verbosity."""

# We have lists (which are really arrays):
ls1 = [1, 2, 3, 4, 5]
ls2 = range(6)			# range is a function that returns lists of ordered data. ls2 == ls1
ls3 = range(2, 10, 3)	# Can do range(start, stop, step-by) == [2, 5, 8]
names = ["Joe", "Andrew", "Chris"]

# Lists can be heterogeneous
ls4 = [1, 2, "stuff", ["pants"]]

# Indices are zero-based.
# Looking up an item in a list is a constant time operation:
joe = names[0]

# As is appending an item to the end:
names.append("Emma")

# and popping from the end:
popped = ls4.pop()

# Popping from anywhere else is slow! Avoid doing so if you can:
slow = ls4.pop(0)

# You can iterate through a list (or any sequence really) with a for loop.
# This is technically a 'for-each' loop.
for i in range(10):
	print i			# Almost anything can be printed. The string conversion function str() will be called on i first.

# If you need the index of the object, use the enumerate function:
for index, name in enumerate(names):
	print index, name

# We also have dictionaries (which are just hash-tables).
# These map 'hashable' data (strings, numbers, and other immutable types) to anything:
ages = {"Joe": 24, "Andrew": 47, "Chris": 23}

# We call the objects before the colon Keys and the objects after Values:
heights = {"Joe": 64, "Andrew": 48, "Chris": 72}

# You can access a value by its key in constant time:
jh = heights["Joe"]		# jh == 64

# And you can add new items to a dictionary like so:
heights["Emma"] = 56

# You can iterate through a dictionary with a for loop by key:
for key in heights:
	print key, heights[key]

# Or by value:
for value in heights.values():
	print value

# Or by key, value pair:
for key, value in heights.items():
	print key, value

# You might also see tuples. Tuples are IMMUTABLE arrays - you can't add to them after
# they're made. But you can use them as dictionary keys (something you can't do with a list).
point1 = (32, 19)
address = ("100 Main Street", "Lexington", "KY")

# You can iterate through these too:
for part in address:
	print part

# You can do multiple assignment (using tuples here)
street, city, state = address
x, y = point1

# Or on ordinary variables and objects:
x, y = 10, 12

# A one-line swap
x, y = y, x

# We have Booleans:
t = True
f = False

# Many items can be converted to Bool. Usually, non-empty or nonzero -> True and empty or zero -> False:
t = bool(23)
f = bool(0)
t = bool([1, 2, 3])
f = bool([])

# You've seen for loops. Other statements include if/elif/else:
if x > y:
	print "x greater"
elif y > x:
	print "y greater"
else:
	print "x, y equal"

# There are also while loops:
count = 0
while count < 10:
	print "Hats"
	count += 1

# break and continue are supported in loops:
s = ""
while True:
	s += "!"
	if len(s) > 100:
		break
print s

# Functions!
def square(x):
	return x * x

def sumofsquares(x, y):
	return square(x) + square(y)

# Recursion is allowed:
def factorial(n):
	if n < 2:
		return 1
	return n * factorial(n - 1)

# As is nesting:
def factorial2(n):
	def loop(accumulator, rest):
		if rest < 2:
			return accumulator
		return loop(accumulator * rest, rest - 1)
	return loop(1, n)

# You can add default values to parameters. If those parameters aren't passed in, the function
# will use the defaults instead:

def make_point(x=0, y=0):
	return (x, y)

origin = make_point()
player1 = make_point(10, 23)
player2 = make_point(x=92, y=-34)

# Functions are objects just like ints or strings. You can assign them into
# variables, pass them as parameters, and return them from functions:
def make_adder(x):
	def adder(n):
		return x + n
	return adder

add5 = make_adder(5)
z = add5(23)			# == 28

# You can pass an arbitrary number of arguments to a function with an *args parameter.
# All the (extra) positional arguments will be collected in args as a tuple.
def add(*nums):
	out = 0
	for i in nums:
		out += i
	return out

sum1 = add(1, 2, 3, 4, 5, 6, 7)
sum2 = add(*range(100))				# You can expand a sequence into arguments using *

# You can pass arbitrary keyword args as well if a function has a **kwargs parameters.
# All the (extra) keyword arguments will be collected in kwargs as a dictionary.
def properties(**kv):
	for key, value in kv.items():
		print key, "maps to", value
	# Functions that don't explicitly return anything return Python's null value None

properties(name="Marvin", age=33, pants="No thanks")

# You can have both if you like. This function can call any function passed with
# its arguments.
def callme(function, *args, **kwargs):
	return function(*args, **kwargs)

sum3 = callme(add, 2, 3, 5)
sum4 = callme(add, *range(10))
callme(properties, stuff="things", something="nothing")

# Everything is an object in Python, and you can make your own too:
class Point2D(object):					# If your class doesn't inherit from anything, make it inherit from object
	def __init__(self, x=0, y=0):		# __init__ (and any other method with double-underscores on either side) is a magic method.
		self.x = x						# Specifically, it constructs an object for you
		self.y = y						# Note that 'self' (the 'this' pointer) is passed explicitly as the first parameter.

	def __str__(self):							# __str__ is called by the str() function. Now we can print this
		return "(%s, %s)" % (self.x, self.y)	# String formatting is sort of like sprintf or printf from C. %s means call str() on the corresponding argument

	def distance(self, other):					# A non-magic method
		import math								# Import library module or things from other scripts with import
		dx = self.x - other.x					# Could also have done 'from math import sqrt' and used 'sqrt' below
		dy = self.y - other.y
		return math.sqrt(dx * dx, dy * dy)		# Use dot-notation to get item from module

p1 = Point2D()			# Initialize a point object with x = 0, y = 0
p2 = Point2D(23, 14)	# Initialize a point object with x = 23, y = 14

print p1, p2			# Call Point2D.__str__ to print objects

# There's a lot more to Python, but this should be enough to recognize what's
# going on. The online documentation is good, so make use of Google. Try
# things in an interactive prompt too!

