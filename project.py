import mysql.connector as mc
import numpy as np
from numpy.random import randint
import time
from threading import Thread
import matplotlib.pyplot as plt
import datetime
import queue

def log(s):
	print(s)

def experiment():
	log('task 1')
	queries = [(1, 'tomato'), (2, 'darkslateblue'), (3, 'darkturquoise')]
	queries = [(30, 'tomato')]

	number_querries = 70
	warmup_threshold = 20
	lambdas = [0.1, 0.15, 0.2, 0.3, 0.5, 1]

	plt.figure()
	for l in lambdas:
		print('Currently proceding to lambda: '+str(l))
		wait_times = np.random.exponential(scale=l,size=number_querries)
		for q, c in queries:
			label = 'Query type '+str(q)
			print(label+': ', end='', flush=True)
			#(queries_per_second, res_time) = threaded_queries(q, wait_times, warmup_threshold)
			(queries_per_second, res_time) = threaded_queue(q, wait_times, warmup_threshold)
			print('{:.3f}q/s, avg {:.3f}s'.format(queries_per_second, res_time))
			plt.plot(queries_per_second, res_time, c=c, marker='.', label=label)
			# let server catch up
			time.sleep(5)

	plt.ylabel('Average response time')
	plt.xlabel('Queries per second')
	plt.legend()
	plt.grid(True)
	plt.show()

def plot_times(times):
	plt.figure()
	plt.plot(range(len(times)), times, c='tomato', marker='.', label='Times')
	plt.ylabel('Time')
	plt.xlabel('Query')
	plt.legend()
	plt.grid(True)
	plt.show()

def thread_query(n, results, i):
	results[i] = query_n(n)

def threaded_queries(q, wait_times, warmup_threshold):
	n = len(wait_times)
	results = np.zeros(n)
	threads = []
	# start requests
	start_time = time.time()
	for i, t in zip(range(n), wait_times):
		thread = Thread(target=thread_query, args=(q, results, i))
		threads.append(thread)
		thread.start()
		time.sleep(t)
	end_time = time.time()
	# wait for requests to finish
	for thread in threads:
		thread.join()
	# make stats
	#log(results)
	res_time = np.mean(results[warmup_threshold:])
	queries_per_sec = n/(end_time-start_time)
	return (queries_per_sec, res_time)


def queue_worker(requests_queue, waiting_time, service_time):
	while True:
		req = requests_queue.get()
		if req is None:
			return

		(i, query, start_time) = req
		waiting_time[i] = time.time()-start_time
		service_time[i] = query_n(query)

def threaded_queue(query, wait_times, warmup_threshold):
	n = len(wait_times)
	waiting_time = np.zeros(n)
	service_time = np.zeros(n)
	#plot_times(wait_times)
	workers = []
	requests_queue = queue.Queue()

	# start workers
	N_WORKERS = 2
	for i in range(N_WORKERS):
		w = Thread(target=queue_worker, args=(requests_queue, waiting_time, service_time))
		w.start()
		workers.append(w)

	# start requests
	start_time = time.time()
	for i, t in zip(range(n), wait_times):
		requests_queue.put((i, query, time.time()))
		time.sleep(t)
	elapsed = time.time()-start_time
	print('queued, ', end='', flush=True)

	# end signal
	for i in range(N_WORKERS):
		requests_queue.put(None)
	# wait for workers to finish
	for w in workers:
		w.join()
	print('finished, ', end='', flush=True)

	# make stats
	#log(waiting_time)
	#log(service_time)

	avg_waiting_time = np.mean(waiting_time[warmup_threshold:])
	avg_service_time = np.mean(service_time[warmup_threshold:])
	print('awt {:.3f}s, ast {:.3f}s, '.format(avg_waiting_time, avg_service_time), end='')
	queries_per_sec = n/elapsed
	return (queries_per_sec, avg_waiting_time+avg_service_time)


def query_n(n):
	if n == 1:
		q = 'SELECT AVG(t.salary) FROM (SELECT salary FROM employees.salaries LIMIT %s OFFSET %s) as t'
		numberOfRows = randint(10, 100)
		startRow = randint(1, 2844047-numberOfRows) # count = 2844047
		params = (numberOfRows, startRow)

	elif n == 2:
		q = 'SELECT * FROM employees.salaries LIMIT %s OFFSET %s'
		numberOfRows = randint(10, 100)
		startRow = randint(1, 2844047-numberOfRows) # count = 2844047
		params = (numberOfRows, startRow)

	elif n == 3:
		q = 'INSERT INTO employees.salaries VALUES (%s,123,%s,%s)'
		from_where = str(np.datetime64('1985-01-01') + randint(365*20))
		to_where = str(np.datetime64('1985-01-01') + randint(365*20))
		employeeNumber = randint(10001, 500000)
		params = (employeeNumber, from_where, to_where)

	elif n == 30:
		acc = 0
		for i in range(10):
			acc += query_n(3)
		return acc

	else:
		print('Querry number {0} not handled'.format(n))
		return
	return query(q, params)

def query(q, params=()):
	try:
		cnx = mc.connect(user='test', password='s0oObGX2oIZeGZ8', host='192.168.0.174', database='employees')
		#cnx = mc.connect(user='test', password='s0oObGX2oIZeGZ8', host='10.0.0.10', port=4242, database='employees')
		# buffered to avoid "Unread result found"
		# see https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone
		cursor = cnx.cursor(buffered=True)
		start_time = time.time()
		#log('start time: '+str(start_time))
		cursor.execute(q, params)
		cnx.commit()
	except (mc.errors.DatabaseError, mc.errors.OperationalError) as err:
		print(err)
	finally:
		#log('closing')
		cursor.close()
		cnx.close()
		end_time = time.time()
		#log('end time: '+str(end_time))
		return end_time-start_time

def clean():
	query('DELETE FROM employees.salaries WHERE salary=123')

if __name__ == "__main__":
	experiment()
