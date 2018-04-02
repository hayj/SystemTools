from systemtools.basics import *
from systemtools.duration import *
import time
from multiprocessing import Process

def f(q):
	time.sleep(getRandomInt(10))
	# time.sleep(1)
	q.put(None)

if __name__ == '__main__':
	nbProcesses = 15
	pbar = ProgressBar(nbProcesses)
	q = pbar.startQueue()
	processes = []
	for i in range(nbProcesses):
		p = Process(target=f, args=(q,))
		processes.append(p)
	for p in processes:
		p.start()
	for p in processes:
		p.join()
	pbar.stopQueue()