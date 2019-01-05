import mysql.connector as mc
import numpy as np
import time
from threading import Thread
import matplotlib.pyplot as plt
import datetime

def log(str):
	print(str)

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

def connection_and_querying(query_number,result):
	try:
		cnx = mc.connect(user='test', password='s0oObGX2oIZeGZ8', host='192.168.0.174', database='employees')
		cursor = cnx.cursor()
		if query_number == 1:
			query = ('SELECT AVG(t.salary) FROM (SELECT salary FROM employees.salaries LIMIT %s OFFSET %s) as t')
			numberOfRows = int(np.random.random()*1000)
			startRow = int(np.random.random()*2000000)
			time_send = time.time()
			cursor.execute(query, (numberOfRows, startRow))
			time_receive = time.time()

		elif query_number == 2:
			query = ('SELECT * FROM employees.salaries LIMIT %s OFFSET %s')
			numberOfRows = 1000000
			startRow = int(np.random.random()*2000000)
			time_send = time.time()
			cursor.execute(query, (numberOfRows, startRow))
			time_receive = time.time()

		elif query_number == 3:
			query = ('INSERT INTO employees.salaries VALUE (%s,123,%s,%s)')
			from_where = datetime.date(1999, 1, 1) # MAYBE CHANGE THAT.
			to_where = datetime.date(1999, 12, 31)
			employeeNumber = 10001+int(np.random.random()*100000)
			time_send = time.time()
			cursor.execute(query, (employeeNumber, from_where, to_where))
			time_receive = time.time()

		else:
			print('Querry number {0} not handled'.format(query_number))
	except mc.Error as err:
		print(err)
	else:
		log('closing')
		cursor.close()
		cnx.close()
		result.append(time_receive-time_send)

if __name__ == "__main__":
	task_1_exp()
