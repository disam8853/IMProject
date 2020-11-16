import os

print(os.path.exists('adjacency.txt'))
file = open('adjacency.txt')
lines = file.readlines()
# line = line[:-1].split(',')
for line in lines:
	line = line[: -1].split(',')
	for i in range(len(line)):
		line[i] = int(line[i])
	print(line)
# print(lines)