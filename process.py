import os
import csv
from decimal import Decimal
from collections import defaultdict
import math
from scipy.misc import logsumexp
import numpy as np
import sys


def get_data(d, filename):
    with open(os.path.join(d, filename)) as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in range(len(data)):
        data[i] = [ float(j) for j in data[i]]
    return data

def get_average(data):
    total = 0.0
    for row in data:
        average_probability = sum(row)/ len(row)
        total += average_probability
    return total

def get_squared_likelihood(data):
    total = 0.0
    for row in data:
        likelihood = sum(row)/ len(row)
        total += math.pow(likelihood, 2)
    return total

def get_product(data):
    total = 0.0
    for row in data:
        probability_of_path = 1.0
        for step in row:
            probability_of_path *= (step )#* 1E+2)
        total += probability_of_path
    return total

def get_log_product(data):
    total = 0.0
    for row in data:
        total += np.exp(np.sum(np.log(row)))
    return total


# print(results)



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: python process.py [resultsdir] [outputfile]")
        exit(1)
    resultsdir = [sys.argv[1]]
    outputfile = sys.argv[2]
    
    results = defaultdict(list)
    result_header = ['filename']
    for d in resultsdir:
        result_header += [d + ".marginal_probability", d+".avg", d+".log"]
        for filename in sorted(os.listdir(d)):
            f = filename.split('.')[0]
            data = get_data(d, filename)
            # print(np.shape(data))
            avg = get_average(data)
            results[f] += [get_product(data), get_average(data), get_log_product(data)]

    with open(outputfile, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(result_header)
        for f in results:
            writer.writerow([f] + results[f])
# print(results)

