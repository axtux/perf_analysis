import mysql.connector as mc
import numpy as np
import time
from threading import Thread
import matplotlib.pyplot as plt
import datetime

def log(s):
	print(s)

def task_1_exp():
	log('task 1')
	queries = [(1, 'tomato'), (2, 'darkslateblue'), (3, 'darkturquoise')]

	number_querries = 120
	warmup_threshold = 20
	lambdas = [i/100 for i in range(5, 55, 5)] # TO CHANGE
	number_lambdas = len(lambdas)

	#unused now
	res_time = np.zeros(number_lambdas)
	queries_per_sec = np.zeros(number_lambdas)

	plt.figure()
	for i in range(number_lambdas):
		print('Currently proceding to lambdas : {0}'.format(lambdas[i]))
		wait_times = np.random.exponential(scale=lambdas[i],size=number_querries)
		for q, c in queries:
			label = 'Query type '+str(q)
			log(label)
			(queries_per_second, res_time) = threaded_queries(q, wait_times, warmup_threshold)
			plt.plot(queries_per_second, res_time, c=c, marker='.', label=label)

	#plt.figure()
	#plt.plot(number_querries_per_second,waiting_time_q1, c='tomato', marker='.', label='Query type 1')
	#plt.plot(number_querries_per_second,waiting_time_q2, c='darkslateblue', marker='.', label='Query type 2')
	#plt.plot(number_querries_per_second,waiting_time_q3, c='darkturquoise', marker='.', label='Querry type 3')
	plt.ylabel('Average response time')
	plt.xlabel('Number of querries per second')
	plt.legend()
	plt.grid(True)
	plt.show()

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
	res_time = np.mean(results[warmup_threshold:])
	queries_per_sec = n/(end_time-start_time)
	return (queries_per_sec, res_time)


def thread_query(n, results, i):
	results[i] = query_n(n)

def query_n(n):
	if n == 1:
		q = 'SELECT AVG(t.salary) FROM (SELECT salary FROM employees.salaries LIMIT %s OFFSET %s) as t'
		numberOfRows = np.random.randint(100, 1000)
		startRow = np.random.randint(1, 2844047-numberOfRows) # count = 2844047
		params = (numberOfRows, startRow)

	elif n == 2:
		q = 'SELECT * FROM employees.salaries LIMIT %s OFFSET %s'
		numberOfRows = np.random.randint(10, 100)
		startRow = np.random.randint(1, 2844047-numberOfRows) # count = 2844047
		params = (numberOfRows, startRow)

	elif n == 3:
		q = 'INSERT INTO employees.salaries VALUES (%s,123,%s,%s)'
		from_where = datetime.date(1999, 1, 1) # TODO MAYBE CHANGE THAT.
		to_where = datetime.date(1999, 12, 31)
		employeeNumber = np.random.randint(10001, 500000)
		params = (employeeNumber, from_where, to_where)

	else:
		print('Querry number {0} not handled'.format(n))
		return
	return query(q, params)

def query(q, params=()):
	try:
		cnx = mc.connect(user='test', password='s0oObGX2oIZeGZ8', host='192.168.0.174', database='employees')
		# buffered to avoid "Unread result found"
		# see https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone
		cursor = cnx.cursor(buffered=True)
		start_time = time.time()
		#log('start time: '+str(start_time))
		cursor.execute(q, params)
		cnx.commit()
	except (mc.errors.InternalError, mc.errors.DatabaseError, mc.errors.OperationalError) as err:
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
	task_1_exp()
