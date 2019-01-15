import queue
import time
from threading import Thread
import random
import matplotlib.pyplot as plt
import numpy as np

def simulated_queue():
	

	number_querries = 20
	warmup_threshold = 10
	
	lambdas = [0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 1]
	#lambdas = [0.05,0.06]
	process_times = [0.05,0.07,0.1]
	colors = ['tomato','darkslateblue','darkturquoise']
	average_time_array = np.zeros((len(process_times),len(lambdas)))
	number_querries_per_second = np.zeros(len(lambdas))
	index = 0
	for l in lambdas:
		wait_times = np.random.exponential(scale=l,size=number_querries)
		for q_t in range(len(process_times)):
			print('Currently proceding to lambda {0} and query type {1}'.format(l,q_t))
			q_server = queue.Queue()
			q_client = queue.Queue()
			thread = Thread(target=server, args=(q_server,q_client,process_times[q_t],False))
			thread.start()

			query_number = 1
			time_beg_total = time.time()
			for waiting_time in wait_times:
				time.sleep(waiting_time)
				sending_time = time.time()
				q_server.put((query_number,sending_time))
				query_number += 1
			time_total_elapsed = time.time() - time_beg_total
			number_querries_per_second[index] += number_querries/(time_total_elapsed*len(process_times))
			q_server.put(('end',0)) 
			print('done with sending\n\n')
			counter = -warmup_threshold
			acc = 0

			while True :
				if not q_client.empty():
					elapsed_time = q_client.get()
					if elapsed_time == 'end':
						break
					counter += 1
					if counter > 0:
						acc += elapsed_time

			average_time = acc/counter
			print('the average time for lambda : {0} is {1}'.format(l,average_time))
			average_time_array[q_t,index] = average_time
		index += 1

	plt.figure()
	for q_t in range(len(process_times)):
		plt.plot(number_querries_per_second,average_time_array[q_t,:], c=colors[q_t], marker='.', label='Query Type {0}'.format(q_t+1))
	plt.ylabel('average_time_array')
	plt.xlabel('number_querries_per_second')
	plt.legend()
	plt.grid(True)
	plt.show()


def server(q_server, q_client, process_time, add_randomness):
	request = None
	waiting_time = process_time
	while(True):
		if not q_server.empty():
			(request,send_time) = q_server.get()
			if request == 'end':
				q_client.put('end')
				break
			print('server receives request : {0}'.format(request))
			if add_randomness :
				waiting_time = process_time + 0 # to change
			time.sleep(waiting_time)
			elapsed_time = time.time() - send_time
			q_client.put(elapsed_time)


if __name__ == "__main__":
	simulated_queue()