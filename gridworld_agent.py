import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

from mdp import MDP 
from map import Map
import pdb


"""
todo:
"""
class GridWorldAgent(object):
	def __init__(self, width=10, height=10, diagonal=True):
		self.map = Map()
		# fill states, transition, actions
		self.width = width
		self.height = height
		self.s, self.t, self.a = self.map.BuildGridWorld(width, height, diagonal)
		self.r = self._CreateRewards()
		self.mdp = MDP(self.s,self.a,self.t,self.r)
		# pdb.set_trace()
		if not self.mdp.Validate():
			raise AssertionError

	def _CreateRewards(self, rewardValues=False, test=True):
		"""
		valsDict (dictionary): maps (x,y) to reward of state
		"""
		# initialize to default
		if not rewardValues:
			rewardValues = {(1,1):10, (self.width, self.height): -10}
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
		if test:
			for state, val in stateRewards.iteritems():
				for action in actions:
					rewards[action, state] = val
		else:
			for curr_state in states: 
				for action in actions: 
					next_state = self.map.makeMove(curr_state, action)
					if next_state in stateRewards:
						rewards[action, curr_state] = stateRewards[next_state]
		return rewards
	def Run(self):
		self.mdp.ValueIteration()
		# self.mdp.BuildPolicy()
		self.mdp.Display(True)
		self.Display()
		

	def getMoves(self):
		policy_mat = self.mdp.policy.transpose()
		policy = [0 for i in self.s]
		for i in range(len(policy)):
			policy[i] = np.argmax(policy_mat[i])
		# print("best move at each state")
		# print(policy)

		return policy

	def Display(self, showpolicy=True):
		data = self.mdp.values.reshape((self.width, self.height))
		# pdb.set_trace()
		fig, ax = plt.subplots()
		ax.matshow(data, cmap='winter')
		for (i, j), z in np.ndenumerate(data):
			ax.text(j, i, '{:0.1f}'.format(z), ha='right', va='top')
		# plt.set(h, 'EdgeColor' = 'b')
		# annotate
		plt.show()


		# labels = {}
		# # pdb.set_trace()
		# values = self.mdp.values.tolist()[0]
		# node_colors = [0 for i in range(self.num_win_chips+1)]
		# # create node labels
		# for state in self.mdp.S:
		# 	labels[state] = str(state) + " \n " + str(round(values[state],2))
		# 	node_colors[state] = -1 * values[state] 
		# # draw nodes
		# nx.draw_networkx_nodes(self.graph, self.graph_pos,node_color=node_colors)
		# nx.draw_networkx_labels(self.graph, self.graph_pos, labels=labels) #, labels = self.node_labels)

		# # choose which edge to show
		# edge_labels = None
		# edge_colors = []
		# if showpolicy:
		# 	moves = self.getMoves()
		# 	edge_list, edge_labels = [], {}
		# 	for i, move in enumerate(moves):
		# 		# if you win
		# 		edge_list.append((i, i + move)) #initial state, state + move
		# 		edge_labels[(i, i + move)] = move
		# 		edge_colors.append('g')
		# 		# if you lose
		# 		edge_list.append((i, max(0, i - move))) #initial state, state + move
		# 		edge_labels[(i, max(0, i - move))] = move
		# 		edge_colors.append('r')
		# 	self.graph.add_edges_from(edge_list)
		# 	# edge_colors = 'r'
		# else: # show probabilities
		# 	self.graph.add_weighted_edges_from(self.edge_probabilites)
		# 	for edge in self.graph.edges():
		# 		# pdb.set_trace()
		# 		edge_colors.append(self.edge_action_labels[edge])
		# 	edge_labels = self.edge_action_labels
		
		# nx.draw_networkx_edges(self.graph, self.graph_pos, edge_color=edge_colors)
		# nx.draw_networkx_edge_labels(self.graph, self.graph_pos, edge_labels=edge_labels)
		# plt.show()
		# # TODO clear edges

if __name__ == "__main__":
	a =  GridWorldAgent(4,4)
	a.Run()





