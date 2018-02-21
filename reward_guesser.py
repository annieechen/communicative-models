import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

from mdp import MDP 
from map import Map
from gridworld_agent import *
import pdb
import random


Actions = range(8)
ActionNames = ["L", "R", "U", "D", "UL", "UR", "DL", "DR"]

class RewardGuesser(object):
	def __init__(self, transition_matrix, states, reward_matrix, action_list, path_list, h, w):
		self.S = states
		self.T = transition_matrix
		self.actual_reward = str(reward_matrix[0])
		self.action_list = action_list
		self.path_list = path_list
		self.h = h
		self.w = w

	def guessReward(self, num_samples):
		sample_matrices = [None] * num_samples
		sample_probabilites = [None] * num_samples
		len_reward = len(self.S)
		# create sample matrices and their vectors
		for i in range(num_samples):
			s = [RewardGuesser.generateRandom() for j in range(len_reward)]
			reward_matrix = self.createRewardMatrix(s)
			sample_matrices[i] = reward_matrix
			sample_probabilites[i] = self.getProbActionsToRewards(reward_matrix)
		total_probabilities = sum(sample_probabilites)
		# now go through and guess each value
		final_list = [None] * len_reward
		for i in range(len_reward):
			r, p , n = 0.0,0.0,0.0
			n_r, n_p, n_n = 0,0,0
			# go through all samples
			for j in range(num_samples):
				if sample_matrices[j][0][i] > 0:
					r += sample_probabilites[j]
					n_r += 1
				elif sample_matrices[j][0][i] < 0:
					p += sample_probabilites[j]
					n_p += 1
				else:
					n  += sample_probabilites[j]
					n_n += 1
			r = r/ (n_r or 1)
			p = p/ (n_p or 1)
			n = n/ (n_n or 1)
			# print(r,p,n)
			# print(n_r, n_p, n_n)
			# get biggest
			if n == max(r,p,n):
				final_list[i] = 0
			elif r == max(r,p,n):
				final_list[i] = 10
			else:
				final_list[i] = -10
		final_matrix = self.createRewardMatrix(final_list)
		# validate probabilites
		max_from_samples = max(sample_probabilites)
		final_probability = self.getProbActionsToRewards(final_matrix)
		print(max_from_samples)
		print(final_probability)
	
		return final_list

		

	# just assuming 1 reward
	def simpleGuessReward(self, action_list, path_list):
		matrix_to_probs = {}
		# try every single state reward #
		for i in range(len(self.S)):
			# initialize a reward matrix to all 0s
			reward_matrix = self.simpleCreateRewards(i, 10)
			prob = self.getProbActionsToRewards(reward_matrix)
			# hash the reward matrix for indexing, only need the 1st row because should be same for every action
			matrix_to_probs[str(reward_matrix[0])] = prob

		return matrix_to_probs

	def simpleCreateRewards(self, i, val):
		rewards = np.full((len(Actions), len(self.S)), 0)
		for action in Actions:
				rewards[action, i] = val
		return rewards

	def createRewardMatrix(self, reward_list):
		rewards = np.full((len(Actions), len(self.S)), 0)
		for action in Actions:
			for i in range(len(reward_list)):
				rewards[action, i] = reward_list[i]
		return rewards

	def getMostProbableRewards(self, matrix_to_probs):
		# get reward matrices with max value
		most_probable = [k for k,v in matrix_to_probs.iteritems() if v == max(matrix_to_probs.values())]
		return most_probable


	def getProbActions(self, reward_matrix):
		mdp = MDP(self.S, Actions, self.T, reward_matrix)
		# pdb.set_trace()
		mdp.ValueIteration()
		mdp.BuildPolicy()
		probabilities = mdp.policy
		# print(probabilities)
		return probabilities

	# def getProbAction(self, probabilities, state, action):
	# 	return pr[state,action]

	def getProbActionsToRewards(self, reward_matrix):
		prob = 1.0
		action_list = self.action_list
		path_list = self.path_list
		# build the polic)es for this reward matrix
		probabilities = self.getProbActions(reward_matrix)
		for i in range(len(action_list)):
			action, state = action_list[i], path_list[i]
			prob *= probabilities[action,state]
		return prob

	def simpleValidate(self, display=False):
		matrix_to_probs = self.simpleGuessReward(self.action_list, self.path_list)
		guesses =  self.getMostProbableRewards(matrix_to_probs)
		print("guesses = " + str(guesses))
		print("actual = " + self.actual_reward)
		return self.actual_reward in guesses

	def validate(self, num_samples=10, display = False):
		final_list = self.guessReward(num_samples)
		guess = str(final_list)
		print("guess = " + str(guess))
		print("actual = " + self.actual_reward)
		if self.actual_reward == guess:
			return True
		# if wrong, choose if want to graph the two values
		if display:
			final_matrix = self.createRewardMatrix(final_list)
			wrong = MDP(self.S, Actions, self.T, final_matrix)
			wrong.ValueIteration()
			self.DisplayValues(wrong.values, self.h, self.w, final_matrix[0])
		return False

	def DisplayValues(self, values, h, w, rewardLocations):
		data = values.reshape((h,w))
		fig, ax = plt.subplots()
		ax.matshow(data, cmap='Greens')
		# add value #s
		for (y, x), z in np.ndenumerate(data):
			ax.annotate( '{:0.1f}'.format(z), xy=(x , y), xycoords='data')#, ha='right', va='top')
		# highlight reward values
		rewards = rewardLocations.reshape((h,w))
		for (y, x), val in np.ndenumerate(rewards):
			if val == 0:
				continue
			if val > 0:
				color = 'green'
			else:
				color = 'red'
			ax.annotate(str(val), xy=(x - 1, y - .7), color=color, backgroundcolor='black')


	# generates a random number with 4 times as much likelyhood first # as second two
	@staticmethod
	def generateRandom(list_of_nums=[0, -10, 10]):
		x = random.randint(1,20)
		if x < 17:
			return list_of_nums[0]
		if x == 18:
			return list_of_nums[1]
		else:
			return list_of_nums[2]


if __name__ == "__main__":
	# a = GridWorldAgent(False, 3,3,rewardValues =  {(1,1):10, (3,3):-10})
	# a.Run()
	# # don't need the coordinate path list 
	# action_list,_, path_list = a.CreatePolicyPath((3,3),max_path_length = 4,  print_path=True)
	# c = RewardGuesser(a.map.T, a.map.S, a.r, action_list, path_list)
	# c.guessReward()

	a = GridWorldAgent(width=4,height=4,rewardValues =  {(1,1):10, (2,2): -10, (3,4):-10})
	a.Run()
	action_list,_, path_list = a.CreatePolicyPath((4,4),max_path_length =7,print_path=True)
	c = RewardGuesser(a.map.T, a.map.S, a.r, action_list, path_list, 4,4)
	c.validate(num_samples = 10, display=True)