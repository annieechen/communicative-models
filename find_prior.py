import numpy as np
import pandas as pd
import heapq
from scipy.stats.stats import pearsonr

data = pd.read_csv('data_for_prior.csv')
people = data['people']
model = data['model']
num_rows = len(data)
TOTAL = 10000 * num_rows
S = 41 * 41

def get_random_vector():
    l = np.random.randint(low=1, high = 10000, size=(num_rows))
    l = np.true_divide(l, TOTAL)
    return l
def get_cor():
    prior = get_random_vector()
    res = (prior)/(prior + model)
    return (pearsonr(res, people)[0], prior)


best_cors = [(0,[]),(0,[]),(0,[]),(0,[]),(0,[])]
min_best_cor = 0
for i in range(100000):
    cor, prior = get_cor()
    cor = abs(cor)
    if cor > min_best_cor:
        x = heapq.heappushpop(best_cors, (cor, str(prior)))[0]
#         print(x)
        min_best_cor = x


for x in best_cors:
	cor, prior = x
	print(cor)
	print(prior)