def closure(max_depth):
	def f(depth):
		if depth >= max_depth:
			return depth
		else:
			return f(depth + 1)
	return f

class CLASS(object):
	def __init__(self, max_depth):
		self.max_depth = max_depth

	def __call__(self, depth):
		if depth >= self.max_depth:
			return depth
		else:
			return self(depth + 1)

class CLASS2(object):
	def __init__(self, max_depth):
		self.max_depth = max_depth

	def __call__(self, depth):
		def do(depth):
			if depth >= self.max_depth:
				return depth
			else:
				return do(depth + 1)
		return do(depth)

m = 1000

a = closure(m)
b = CLASS(m)
c = CLASS2(m)

a(0)
# b(0) # this one keks
c(0)

from timeit import default_timer as timer

start = timer(); [a(0) for _ in range(10000)] ; end = timer() ; print(end - start)
start = timer(); [c(0) for _ in range(10000)] ; end = timer() ; print(end - start)

# 2.988696776010329
# 3.2523498149967054