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
	number_querries = 120
	warmup_threshold = 20
	lambdas = [i/100 for i in range(5, 55, 5)] # TO CHANGE
	number_lambdas = len(lambdas)
	waiting_time_q1 = np.zeros(number_lambdas)
	waiting_time_q2 = np.zeros(number_lambdas)
	waiting_time_q3 = np.zeros(number_lambdas)
	number_querries_per_second = np.zeros(number_lambdas)
	for i in range(len(lambdas)):
		print('Currently proceding to lambdas : {0}'.format(lambdas[i]))
		wait_times = np.random.exponential(scale=lambdas[i],size=number_querries)
		result_q1 = [ ]
		result_q2 = [ ]
		result_q3 = [ ]
		time_begining_exp = time.time()
		for t in wait_times:
			thread_q1 = Thread(target=connection_and_querying, args=(1, result_q1))
			thread_q2 = Thread(target=connection_and_querying, args=(2, result_q2))
			thread_q3 = Thread(target=connection_and_querying, args=(3, result_q3))
			time.sleep(t)
			thread_q1.start()
			thread_q2.start()
			thread_q3.start()
		time_end_exp = time.time()
		number_querries_per_second[i] = number_querries/(time_end_exp-time_begining_exp)

		for waiting_time in result_q1[warmup_threshold:]:
			waiting_time_q1[i]+= waiting_time/(number_querries-warmup_threshold)
		for waiting_time in result_q2[warmup_threshold:]:
			waiting_time_q2[i]+= waiting_time/(number_querries-warmup_threshold)
		for waiting_time in result_q3[warmup_threshold:]:
			waiting_time_q3[i]+= waiting_time/(number_querries-warmup_threshold)

	plt.figure()
	plt.plot(number_querries_per_second,waiting_time_q1, c='tomato', marker='.', label='Query type 1')
	plt.plot(number_querries_per_second,waiting_time_q2, c='darkslateblue', marker='.', label='Query type 2')
	plt.plot(number_querries_per_second,waiting_time_q3, c='darkturquoise', marker='.', label='Querry type 3')
	plt.ylabel('Average response time')
	plt.xlabel('Number of querries per second')
	plt.legend()
	plt.grid(True)
	plt.show()

def thread_query(n, result, i):
	result[i] = query_n(n)

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
		log('start time: '+str(start_time))
		cursor.execute(q, params)
		cnx.commit()
	except (mc.errors.InternalError, mc.errors.DatabaseError, mc.errors.OperationalError) as err:
		print(err)
	finally:
		log('closing')
		cursor.close()
		cnx.close()
		end_time = time.time()
		log('end time: '+str(end_time))
		return end_time-start_time

def clean():
	query('DELETE FROM employees.salaries WHERE salary=123')

if __name__ == "__main__":
	task_1_exp()
