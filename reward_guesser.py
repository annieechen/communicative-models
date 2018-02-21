import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

from mdp import MDP 
from map import Map
from gridworld_agent import *
import pdb


Actions = range(8)
ActionNames = ["L", "R", "U", "D", "UL", "UR", "DL", "DR"]

class RewardGuesser(object):
	def __init__(self, transition_matrix, states, reward_matrix):
		self.S = states
		self.T = transition_matrix
		self.actual_reward = str(reward_matrix[0])

	def guessReward(self, action_list, path_list):
		matrix_to_probs = {}
		# try every single state reward #
		for i in range(len(self.S)):
			# initialize a reward matrix to all 0s
			reward_matrix = self.createRewards(i, 10)
			prob = self.getProbActionsToRewards(reward_matrix, action_list, path_list)
			# hash the reward matrix for indexing, only need the 1st row because should be same for every action
			matrix_to_probs[str(reward_matrix[0])] = prob

		return matrix_to_probs

	def getMostProbableRewards(self, matrix_to_probs):
		# get reward matrices with max value
		most_probable = [k for k,v in matrix_to_probs.iteritems() if v == max(matrix_to_probs.values())]
		return most_probable

	def createRewards(self, i, val):
		rewards = np.full((len(Actions), len(self.S)), 0)
		for action in Actions:
				rewards[action, i] = val
		return rewards


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

	def getProbActionsToRewards(self, reward_matrix, action_list, path_list):
		prob = 1.0
		# build the polic)es for this reward matrix
		probabilities = self.getProbActions(reward_matrix)
		for i in range(len(action_list)):
			action, state = action_list[i], path_list[i]
			prob *= probabilities[action,state]
		return prob

	def validate(self, action_list, path_list, display=False):
		matrix_to_probs = self.guessReward(action_list, path_list)
		guesses =  self.getMostProbableRewards(matrix_to_probs)
		print("guesses = " + str(guesses))
		print("actual = " + self.actual_reward)
		return self.actual_reward in guesses

if __name__ == "__main__":
	a = GridWorldAgent(False, 3,3,rewardValues =  {(1,1):10})
	a.Run()
	pdb.set_trace()
	# don't need the coordinate path list 
	action_list,_, path_list = a.CreatePolicyPath((3,3),max_path_length = 4,  print_path=True)
	c = RewardGuesser(a.map.T, a.map.S)
	c.guessReward(action_list, path_list)