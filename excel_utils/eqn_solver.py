
import pip
try:
	from sympy import Symbol, solve
except ModuleNotFoundError:
	pip.main(["install", "sympy"])
	from sympy import Symbol, solve
	
	
x = Symbol("x")
y = Symbol("y")


import math
print(solve([1992*(1+x)**(1/2) - 2027],x)[0][0])
print(solve([1992*math.exp(1)**(x/2) - 2027],x)[0][0])
