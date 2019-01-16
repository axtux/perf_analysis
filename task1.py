import numpy as np
import time
import matplotlib.pyplot as plt
import query
import config

def log(s):
	print(s)

def experiment():
	log('task 1')

	a_qps = {}
	a_avg = {}
	a_low = {}
	a_high = {}
	# create one tab per query
	for q in query.QUERIES:
		a_qps[q] = []
		a_avg[q] = []
		a_low[q] = []
		a_high[q] = []

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
			a_low[q].append(avg-min)
			a_high[q].append(max-avg)
			# let server catch up
			time.sleep(2)

	for q, c in zip(query.QUERIES, config.COLORS):
		plt.errorbar(a_qps[q], a_avg[q], c=c, marker='.', label='Query type '+str(q), yerr=(a_low[q], a_high[q]))
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


"""results
Currently proceding to lambda: 0.03
	Query type 1: q/s, min, avg, max = 29.331, 3.431, 18.750, 32.951
	Query type 2: q/s, min, avg, max = 29.443, 0.319, 25.146, 41.211
	Query type 3: q/s, min, avg, max = 29.405, 0.010, 0.032, 0.068
	Query type 4: q/s, min, avg, max = 26.089, 0.016, 0.054, 0.105
Currently proceding to lambda: 0.1
	Query type 1: q/s, min, avg, max = 9.546, 1.478, 16.525, 31.892
	Query type 2: q/s, min, avg, max = 9.546, 1.396, 19.494, 38.956
	Query type 3: q/s, min, avg, max = 9.556, 0.009, 0.014, 0.044
	Query type 4: q/s, min, avg, max = 9.187, 0.013, 0.027, 0.112
Currently proceding to lambda: 0.15
	Query type 1: q/s, min, avg, max = 6.253, 0.585, 9.671, 22.037
	Query type 2: q/s, min, avg, max = 6.252, 0.474, 18.224, 35.071
	Query type 3: q/s, min, avg, max = 6.255, 0.009, 0.012, 0.024
	Query type 4: q/s, min, avg, max = 6.106, 0.012, 0.023, 0.084
Currently proceding to lambda: 0.2
	Query type 1: q/s, min, avg, max = 5.026, 0.015, 8.856, 17.819
	Query type 2: q/s, min, avg, max = 5.025, 0.209, 15.349, 29.826
	Query type 3: q/s, min, avg, max = 5.026, 0.009, 0.013, 0.025
	Query type 4: q/s, min, avg, max = 4.928, 0.017, 0.023, 0.048
Currently proceding to lambda: 0.3
	Query type 1: q/s, min, avg, max = 3.598, 0.054, 3.361, 8.272
	Query type 2: q/s, min, avg, max = 3.598, 0.044, 7.218, 16.722
	Query type 3: q/s, min, avg, max = 3.598, 0.009, 0.012, 0.020
	Query type 4: q/s, min, avg, max = 3.546, 0.012, 0.022, 0.043
Currently proceding to lambda: 0.5
	Query type 1: q/s, min, avg, max = 2.058, 0.036, 0.836, 2.167
	Query type 2: q/s, min, avg, max = 2.057, 0.042, 2.338, 8.289
	Query type 3: q/s, min, avg, max = 2.058, 0.009, 0.012, 0.023
	Query type 4: q/s, min, avg, max = 2.041, 0.017, 0.023, 0.110
Currently proceding to lambda: 1
	Query type 1: q/s, min, avg, max = 1.116, 0.019, 0.565, 1.315
	Query type 2: q/s, min, avg, max = 1.116, 0.052, 0.888, 2.123
	Query type 3: q/s, min, avg, max = 1.116, 0.009, 0.011, 0.022
	Query type 4: q/s, min, avg, max = 1.111, 0.016, 0.026, 0.111
"""
