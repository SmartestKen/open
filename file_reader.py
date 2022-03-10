import sys

if len(sys.argv) == 1:
	sys.exit("Require filename as argument")
	
# print first line, each line first few characters and last few
with open(sys.argv[1]) as myfile:
    head = [next(myfile) for x in range(200)]
print(head)

