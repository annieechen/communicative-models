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
	def __init__(self, transition_matrix, states):
		self.S = states
		self.T = transition_matrix

	def guessReward(self, action_list, path_list):
		rewardsToProbs = {}
		# try every single state reward #
		for i in range(len(self.S)):
			# initialize a reward matrix to all 0s
			reward_matrix = self.createRewards(i, 20)
			prob = self.getProbActionsToRewards(reward_matrix, action_list, path_list)
			rewardsToProbs[i] = prob

		# get reward function with highest probability
		max_prob = max(rewardsToProbs, key=rewardsToProbs.get)
		max_keys = [x for x, v in rewardsToProbs.iteritems() if v == rewardsToProbs[max_prob]]
		print("best prob states " + str(max_keys) + "=" + str(max_prob))
		return rewardsToProbs

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

if __name__ == "__main__":
	a = GridWorldAgent(False, 3,3,rewardValues =  {(1,1):10})
	a.Run()
	pdb.set_trace()
	# don't need the coordinate path list 
	action_list,_, path_list = a.CreatePolicyPath((3,3),max_path_length = 4,  print_path=True)
	c = RewardGuesser(a.map.T, a.map.S)
	c.guessReward(action_list, path_list)