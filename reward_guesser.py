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

	

	# just assuming 1 reward
	def simpleGuessReward(self, action_list, path_list):
		final_probs = np.zeros(len(self.S))
		# try every single state reward #
		for i in range(len(self.S)):
			prob = self.getProbActionsToRewards(i)
			final_probs[i] = prob

		return final_probs



	def getProbActions(self, reward_location):
		# mdp = MDP(self.S, Actions, self.T, reward_matrix)
		# # pdb.set_trace()
		# mdp.ValueIteration()
		# mdp.BuildPolicy()
		reward_dict = {reward_location:10}
		a = GridWorldAgent(width=self.w,height=self.h,rewardValues = reward_dict)
		a.Run(get_moves = False)
		probabilities = a.mdp.policy
		# print(probabilities)
		return probabilities

	# def getProbAction(self, probabilities, state, action):
	# 	return pr[state,action]

	def getProbActionsToRewards(self, reward_location):
		prob = 1.0
		action_list = self.action_list
		path_list = self.path_list
		# build the policies for this reward matrix
		probabilities = self.getProbActions(reward_location)
		reward_seen = False
		for i in range(len(action_list)):
			action, state = action_list[i], path_list[i]
			if state == reward_location:
				reward_seen = True
			if reward_seen:
				prob *= 1.0/len(ActionNames)
			else:
				prob *= probabilities[action,state]
		return prob

	def getMarginalProb(self):
		final_probs = self.simpleGuessReward(self.action_list, self.path_list)
		s = np.sum(final_probs)
		print(s)
		return s


	def simpleValidate(self, display=False):
		matrix_to_probs, final_probs = self.simpleGuessReward(self.action_list, self.path_list)
		print(np.var(final_probs))
		print(np.sum(final_probs))
		guesses =  self.getMostProbableRewards(matrix_to_probs)
		print("guesses = " + str(guesses))
		print("actual = " + self.actual_reward)
		return self.actual_reward in guesses


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
			ax.annotate(str(val), xy=(x, y - .3), color=color, backgroundcolor='black')



	def getMostProbableRewards(self, matrix_to_probs):
		# get reward matrices with max value
		most_probable = [k for k,v in matrix_to_probs.iteritems() if v == max(matrix_to_probs.values())]
		return most_probable

	############################################
 	### fancier version with expected values ### 
 	############################################
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
			expected_value = 0.0
			# go through all samples
			for j in range(num_samples):
				expected_value += sample_matrices[j][0][i] * sample_probabilites[j]
			final_list[i] = expected_value * 10
		final_matrix = self.createRewardMatrix(final_list)
		# validate probabilites
		max_from_samples = max(sample_probabilites)
		final_probability = self.getProbActionsToRewards(final_matrix)
		print(max_from_samples)
		print(final_probability)

		return final_list
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

		
	def createRewardMatrix(self, reward_list):
		rewards = np.full((len(Actions), len(self.S)), 0)
		for action in Actions:
			for i in range(len(reward_list)):
				rewards[action, i] = reward_list[i]
		return rewards

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