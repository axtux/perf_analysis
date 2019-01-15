import mysql.connector as mc
import numpy as np
from numpy.random import randint
import time
from threading import Thread
import config

QUERIES = [1, 2, 3, 4]

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
		# single entry with index
		q = 'SELECT * FROM employees.employees WHERE emp_no > %s ORDER BY emp_no LIMIT 1'
		next_no = randint(10001, 500000)
		params = (next_no,)

	elif n == 4:
		values = emp_values()
		# insert multiple entries in one request
		for i in range(100):
			values += ', '+emp_values()
		q = 'INSERT INTO employees.employees VALUES '+values
		params = ()

	else:
		print('Querry number {0} not handled'.format(n))
		return
	return query(q, params)

def emp_values():
	emp_no = randint(500000, 2147483647)
	birth_date = str(np.datetime64('1950-01-01') + randint(365*50))
	first_name = 'FirstName'
	last_name = 'LastName'
	gender = str(np.random.choice(('M', 'F')))
	hire_date = str(np.datetime64('1985-01-01') + randint(365*30))
	return '({0}, "{1}", "{2}", "{3}", "{4}", "{5}")'.format(emp_no, birth_date, first_name, last_name, gender, hire_date)

def query(q, params=()):
	cnx = None
	cursor = None
	try:
		cnx = mc.connect(user=config.USER, password=config.PWD, host=config.HOST, database=config.DB)
		# buffered to avoid "Unread result found"
		# see https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone
		cursor = cnx.cursor(buffered=True)
		start_time = time.time()
		#log('start time: '+str(start_time))
		cursor.execute(q, params)
		cnx.commit()
	# catch Duplicate entry errors (id is random and collisions are possible)
	except mc.errors.IntegrityError as e:
		if not 'Duplicate' in e.msg:
			print(e.msg)
	finally:
		#log('closing')
		if not cursor is None:
			cursor.close()
		if not cnx is None:
			cnx.close()
		end_time = time.time()
		#log('end time: '+str(end_time))
	return end_time-start_time

def clean():
	query('DELETE FROM employees.employees WHERE emp_no>499999')

if __name__ == "__main__":
	experiment()
