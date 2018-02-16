import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

from mdp import MDP 
from map import Map
import pdb


class GridWorldAgent(object):
	def __init__(self, rewardWhenReached = False, width=10, height=10, diagonal=True, rewardValues = None):
		self.map = Map(diagonal=True)
		# fill states, transition, actions
		self.width = width
		self.height = height
		self.s, self.t, self.a = self.map.BuildGridWorld(width, height, diagonal)
		self.rewardWhenReached = rewardWhenReached

		# list of coordinates(1 indexed) with rewards
		self.rewardLocations = None
		self.r = self._CreateRewards(rewardValues)
		self.mdp = MDP(self.s,self.a,self.t,self.r)
		self.policy = None
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
		self.rewardLocations = rewardValues
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

	def Run(self, display=False):
		self.mdp.ValueIteration()
		self.mdp.BuildPolicy()
		self.getMoves()
		if display:
			self.Display()
		

	def getMoves(self, print_moves = True):
		policy_mat = self.mdp.policy.transpose()
		policy = [0 for i in self.s]
		for i in range(len(policy)):
			policy[i] = np.argmax(policy_mat[i])
		if print_moves:
			print("best move at each state")
			policy_names = self.map.GetActionNames(policy)
			print(policy_names.reshape((self.height, self.width)))
		self.policy = policy
		return policy


	def Display(self, showpolicy=False, path_list=None):
		data = self.mdp.values.reshape((self.height, self.width))
		fig, ax = plt.subplots()
		ax.matshow(data, cmap='Greens')
		if showpolicy:
			for (y, x), z in np.ndenumerate(data):
				if (x + 1, y + 1,) in path_list:
					ax.annotate( '{:0.1f}'.format(z), xy=(x , y), xycoords='data', backgroundcolor='white')
				else:
					ax.annotate( '{:0.1f}'.format(z), xy=(x , y), xycoords='data')
		# don't change colors
		else:
			for (y, x), z in np.ndenumerate(data):
				ax.annotate( '{:0.1f}'.format(z), xy=(x , y), xycoords='data')#, ha='right', va='top')
		# highlight reward values
		for state, val in self.rewardLocations.iteritems():
			x,y = state
			if val > 0:
				color = 'green'
			else:
				color = 'red'
			ax.annotate('{:0.1f}'.format(val), xy=(x - 1, y - .7), color=color, backgroundcolor='black')
		plt.show()


	# start_coordinates = (x,y) tuple
	def CreatePolicyPath(self, start_coordinates, max_path_length=10, print_path=False):
		# if getMoves hasn't been called yet
		if not self.policy:
			self.getMoves(False)
		curr_state = self.map.GetRawStateNumber(start_coordinates)
		num_steps = 0
		path_list = []
		action_list = []
		while num_steps < max_path_length:
			# move to next state
			best_action = self.policy[curr_state]
			path_list.append(self.map.GetCoordinates(curr_state))
			action_list.append(best_action)
			curr_state = self.map.makeMove(curr_state, best_action)
			num_steps += 1
		if print_path:
			for i in range(max_path_length):
				print(str(path_list[i]) + str(action_list[i]))
		self.Display(showpolicy = True, path_list = path_list)
		return action_list, path_list



if __name__ == "__main__":
	a =  GridWorldAgent(width=3,height=4, rewardValues = {(2,4):10, (3,1): -20})
	a.Run(display = True)





