import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

from mdp import MDP 
from map import Map
import pdb


class GridWorldAgent(object):
	def __init__(self, rewardWhenReached, width=10, height=10, diagonal=True, rewardValues = None):
		self.map = Map()
		# fill states, transition, actions
		self.width = width
		self.height = height
		self.s, self.t, self.a = self.map.BuildGridWorld(width, height, diagonal)
		self.rewardWhenReached = rewardWhenReached
		self.r = self._CreateRewards(rewardValues)
		self.mdp = MDP(self.s,self.a,self.t,self.r)
		# pdb.set_trace()
		if not self.mdp.Validate():
			raise AssertionError

	# rewardWhenReached = true, then
	def _CreateRewards(self, rewardValues=False):
		"""
		valsDict (dictionary): maps (x,y) to reward of state
		"""
		# initialize to default
		if not rewardValues:
			rewardValues = {(1,1):10, (self.width,self.height): -10}
		states = self.s
		actions = self.a
		rewards = np.full((len(self.a), len(self.s)), 0)
		# transform coordinates to states
		stateRewards = {}
		for coord, val in rewardValues.iteritems():
			state = self.map.GetRawStateNumber(coord)
			print("coord: " + str(coord) + " state: " + str(state) + " val: " + str(val))
			stateRewards[state] = val
		# loop through all states and actions, if they reach a reward, set it
		if self.rewardWhenReached:
			for curr_state in states: 
				for action in actions: 
					next_state = self.map.makeMove(curr_state, action)
					if next_state in stateRewards:
						rewards[action, curr_state] = stateRewards[next_state]
		# any action they take in reward state = reward
		else:
			for state, val in stateRewards.iteritems():
				for action in actions:
					rewards[action, state] = val
		
		return rewards
	def Run(self):
		self.mdp.ValueIteration()
		self.mdp.BuildPolicy()
		self.getMoves()
		self.Display()
		

	def getMoves(self, print_moves = True):
		policy_mat = self.mdp.policy.transpose()
		policy = [0 for i in self.s]
		for i in range(len(policy)):
			policy[i] = np.argmax(policy_mat[i])
		if print_moves:
			print("best move at each state")
			policy_names = self.map.GetActionNames(policy)
			print(policy_names.reshape((self.width, self.height)))
		self.policy = policy
		return policy

	def Display(self, showpolicy=True):
		data = self.mdp.values.reshape((self.width, self.height))
		# pdb.set_trace()
		fig, ax = plt.subplots()
		ax.matshow(data, cmap='Greens')
		for (i, j), z in np.ndenumerate(data):
			ax.text(j, i, '{:0.1f}'.format(z), ha='right', va='top')
		# plt.set(h, 'EdgeColor' = 'b')
		# annotate
		plt.show()


	# start_coordinates = (x,y) tuple
	def CreatePolicyPath(self, start_coordinates, max_path_length=10):
		# if getMoves hasn't been called yet
		if not self.policy:
			self.getMoves(False)
		curr_state = self.map.GetRawStateNumber(start_coordinates)
		num_steps = 0
		path_list = []
		while num_steps < max_path_length:
			path_list.append(curr_state)
			# move to next state
			best_action = 
			num_steps += 1



if __name__ == "__main__":
	a =  GridWorldAgent(6,6)
	a.Run()





