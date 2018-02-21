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
	def __init__(self, transition_matrix, states, reward_matrix, action_list, path_list):
		self.S = states
		self.T = transition_matrix
		self.actual_reward = str(reward_matrix[0])
		self.action_list = action_list
		self.path_list = path_list

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
				elif sample_matrices[j][0][i] < 0:
					p += sample_probabilites[j]
				else:
					n  += sample_probabilites[j]
			# get biggest
			if r == max(r,p,n):
				final_list[i] = 10
			elif p == max(r,p,n):
				final_list[i] = -10
			else:
				final_list[i] = 0
		final_matrix = self.createRewardMatrix(final_list)
		# validate probabilites
		max_from_samples = max(sample_probabilites)
		final_probability = self.getProbActionsToRewards(final_matrix)
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

	def validate(self, num_samples=10):
		guess = str(self.guessReward(num_samples))
		print("guess = " + str(guess))
		print("actual = " + self.actual_reward)
		return self.actual_reward == guess


	# generates a random number with 4 times as much likelyhood first # as second two
	@staticmethod
	def generateRandom(list_of_nums=[0, -10, 10]):
		x = random.randint(1,10)
		if x < 8:
			return list_of_nums[0]
		if x == 9:
			return list_of_nums[1]
		else:
			return list_of_nums[2]


if __name__ == "__main__":
	a = GridWorldAgent(False, 3,3,rewardValues =  {(1,1):10, (3,3):-10})
	a.Run()
	# don't need the coordinate path list 
	action_list,_, path_list = a.CreatePolicyPath((3,3),max_path_length = 4,  print_path=True)
	c = RewardGuesser(a.map.T, a.map.S, a.r, action_list, path_list)
	c.guessReward()