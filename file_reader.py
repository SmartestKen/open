import sys

if len(sys.argv) == 1:
	sys.exit("Require filename as argument")
	
# print first line, each line first few characters and last few
with open(sys.argv[1]) as myfile:
	head = []
	for x in range(200):
		line = next(myfile)
		if len(line) < 60:
			print(line, end='')
		else:
			print(line[:30] + "..." + line[-30:], end='')

