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

	a_qps = {}
	a_avg = {}
	a_errors = {}
	# create one tab per query
	for q in query.QUERIES:
		a_qps[q] = []
		a_avg[q] = []
		a_errors[q] = []

	plt.figure()
	for l in config.LAMBDAS:
		print('Currently proceding to lambda: '+str(l))
		wait_times = np.random.exponential(scale=l,size=config.N_QUERIES)
		for q in query.QUERIES:
			print('\tQuery type '+str(q)+': ', end='', flush=True)
			# making queries
			(qps, min, avg, max) = query.threaded_queries(q, wait_times, config.THRESHOLD)
			print('q/s, min, avg, max = {:.3f}, {:.3f}, {:.3f}, {:.3f}'.format(qps, min, avg, max))
			# TODO add error bars https://matplotlib.org/api/_as_gen/matplotlib.pyplot.errorbar.html
			a_qps[q].append(qps)
			a_avg[q].append(avg)
			a_errors[q].append((avg-min, max-avg))
			# let server catch up
			time.sleep(2)

	for q, c in zip(query.QUERIES, colors):
		plt.errorbar(a_qps[q], a_avg[q], c=c, marker='.', label='Query type '+str(q), yerr=a_errors[q])
	print('\nLaTeX tab:')
	for l, i in zip(config.LAMBDAS, range(len(config.LAMBDAS))):
		print('\t'+str(l)+' & '+str('{:.3f}'.format(a_qps[1][i])), end='')
		for q in query.QUERIES:
			print(' & '+str('{:.3f}'.format(a_avg[q][i])), end='')
		print('\\\\')

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
