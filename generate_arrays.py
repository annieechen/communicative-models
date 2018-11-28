"""
This script generates all the policies for a gridworld of a certain width, height, and softmax
"""
from gridworld_agent import *
from multiprocessing import Pool
import numpy as np
import os
import sys

# reward location from 0 to n
def gen_and_save_policy(reward_location):
	filename = os.path.join(dir_name, "%04d" % (reward_location))
	if not os.path.isfile(filename + ".npy"):
		agent = GridWorldAgent(width=width, height=height, rewardValues={reward_location: 10}, softmax=softmax, diagonal=diag)
		agent.Run()
		np.save(os.path.join(dir_name, "%04d" % (reward_location)), agent.mdp.policy)

if __name__ == '__main__':
	if len(sys.argv) < 5:
		print("usage: generate_arrays [width] [height] [softmax] [num processes] [-d for diag]")
		exit(1)
	global width, height, softmax, diag
	width = int(sys.argv[1])
	height = int(sys.argv[2])
	softmax = float(sys.argv[3])
	num_processes = int(sys.argv[4])
	if len(sys.argv) == 6 and sys.argv[5] == "-d":
		diag = True
	else:
		diag = False 

	# create directory, put info in it
	global dir_name
	dir_name = "policies_%s_%s_%s" %(width, height, softmax)
	if diag:
		dir_name += '_d'
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	with open(os.path.join(dir_name, 'info.txt'), 'wb') as info_file:
		info_file.write("Width: %s\nHeight: %s\nSoftmax: %s\nDiag: %s\n" %(width, height, softmax, diag))
	total_policies = range(width * height)

	pool = Pool(processes=num_processes)
	pool.map(gen_and_save_policy, total_policies)

