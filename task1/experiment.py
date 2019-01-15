import numpy as np
import time
import matplotlib.pyplot as plt
import query
import config

def log(s):
	print(s)

def experiment():
	log('task 1')
	colors = ['tomato', 'darkslateblue', 'darkturquoise', 'darkgreen']

	plt.figure()
	for l in config.LAMBDAS:
		print('Currently proceding to lambda: '+str(l))
		wait_times = np.random.exponential(scale=l,size=config.N_QUERIES)
		for q, c in zip(query.QUERIES, colors):
			label = '\tQuery type '+str(q)
			print(label+': ', end='', flush=True)
			# making queries
			(queries_per_second, res_time) = query.threaded_queries(q, wait_times, config.THRESHOLD)
			print('{:.3f}q/s, avg {:.3f}s'.format(queries_per_second, res_time))
			# TODO add error bars https://matplotlib.org/api/_as_gen/matplotlib.pyplot.errorbar.html
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

if __name__ == "__main__":
	experiment()
