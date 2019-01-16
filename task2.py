import queue
import time
from threading import Thread
import random
import matplotlib.pyplot as plt
import numpy as np

import config

def simulated_queue():

	process_times = [0.691, 0.557, 0.012, 0.025]
	avg_times = np.zeros((len(process_times),len(config.LAMBDAS)))
	queries_per_second = np.zeros(len(config.LAMBDAS))
	index = 0
	for l in config.LAMBDAS:
		print('Currently proceding to lambda: '+str(l))
		wait_times = np.random.exponential(scale=l,size=config.N_QUERIES)
		for q_t in range(len(process_times)):
			print('\tQuery type '+str(q_t)+': ', end='', flush=True)
			q_server = queue.Queue(maxsize=20)
			q_client = queue.Queue()
			thread_1 = Thread(target=server, args=(q_server,q_client,process_times[q_t],False))
			thread_2 = Thread(target=server, args=(q_server,q_client,process_times[q_t],False))
			thread_1.start()
			thread_2.start()
			query_number = 1
			time_beg_total = time.time()
			for waiting_time in wait_times:
				time.sleep(waiting_time)
				sending_time = time.time()
				q_server.put((query_number,sending_time))
				query_number += 1
			time_total_elapsed = time.time() - time_beg_total
			queries_per_second[index] += config.N_QUERIES/(time_total_elapsed*len(process_times))
			q_server.put(('end',0))
			print('sent, ', end='', flush=True)
			counter = -config.THRESHOLD
			acc = 0

			while True:
				elapsed_time = q_client.get()
				if elapsed_time == 'end':
					break
				counter += 1
				if counter > 0:
					acc += elapsed_time

			average_time = acc/counter
			print('{:.3f}'.format(average_time))
			avg_times[q_t,index] = average_time
		index += 1

	plt.figure()
	plt.subplot(211)
	for q_t in range(2):
		plt.plot(queries_per_second,avg_times[q_t,:], c=config.COLORS[q_t], marker='.', label='Query Type {0}'.format(q_t+1))
	plt.ylabel('Average time')
	plt.xlabel('Queries/second')
	plt.legend()
	plt.grid(True)
	plt.subplot(212)
	for q_t in range(2,len(process_times)):
		plt.plot(queries_per_second,avg_times[q_t,:], c=config.COLORS[q_t], marker='.', label='Query Type {0}'.format(q_t+1))
	plt.ylabel('Average time')
	plt.xlabel('Queries/second')
	plt.legend()
	plt.grid(True)
	plt.show()


def server(q_server, q_client, process_time, add_randomness):
	waiting_time = process_time
	while True:
		(request,send_time) = q_server.get()
		if request == 'end':
			q_client.put('end')
			break
		#print('server receives request : {0}'.format(request))
		if add_randomness :
			waiting_time = process_time + np.random.normal(scale=0.005)
		time.sleep(waiting_time)
		elapsed_time = time.time() - send_time
		q_client.put(elapsed_time)


if __name__ == "__main__":
	simulated_queue()
