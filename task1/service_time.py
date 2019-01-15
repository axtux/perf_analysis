import time
import numpy as np

import query


def service_time(n):
	for q in query.QUERIES:
		times = np.zeros(n)
		label = 'Query type '+str(q)
		print(label+': ', end='', flush=True)
		for i in range(n):
			times[i] = query.query_n(q)
			time.sleep(5)
		min, avg, max = np.min(times), np.mean(times), np.max(times)
		print('min/avg/max = {:.3f}/{:.3f}/{:.3f}'.format(min, avg, max))
		time.sleep(5)

if __name__ == "__main__":
	service_time(20)
