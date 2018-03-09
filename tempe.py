from gridworld_agent import *
from reward_guesser import *
import csv
import os
import json
from multiprocessing import Pool




fs = []




def f(filename):
	b = GridWorldAgent(width=32,height=32,rewardValues =  {1:10})
    with open(os.path.join("scaled_data", filename)) as csvfile:
	    reader = csv.reader(csvfile)
	    data = list(reader)
	print(filename)
    data = [(int(x),int(y)) for (x,y) in data]
    action_list, path_list = b.takeListGetPath(data)
    c = RewardGuesser(b.map.T, b.map.S, b.r, action_list, path_list, 32,32)
    res = c.getMarginalProb()
    print(res)
    return res







if __name__ == '__main__':
	for filename in os.listdir("scaled_data"):
	if filename.startswith('e'):
		fs.append(filename)
    pool = Pool(processes=4)              # start 4 worker processes
    result = pool.map(f, fs)
    print result

