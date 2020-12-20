import time
from multiprocess import Process

def looping():
	i = 0
	while(1):
		i += 1
		time.sleep(3)
		print(i)

def main():
	print("this is main function~")
	time.sleep(6)
	print("end of main function~")
if __name__ == "__main__":
	p1 = Process(target = looping)
	p2 = Process(target = main)
	p1.start()
	p2.start()
	p1.join()
	p2.join()

# file = open('path/result_20201116_032636.json')
# r = file.read()
# r = json.loads(r)
# methods = []
# keys = r.keys()
# for key in keys:
# 	methods.append({key : r[key]})
# print(methods)