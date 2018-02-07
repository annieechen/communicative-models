import numpy as np
import matplotlib.pyplot as plt
import networkx as nx 

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
		self.s, self.t, self.A = self.map.BuildGridWorld(width, height, diagonal)
		self.r = _CreateRewards(self,)
		self.mdp = MDP(self.s,self.a,self.t,self.r)
		if not self.mdp.Validate():
			raise AssertionError
		self.initDisplay()

	def _CreateRewards(self, valsDict = {}):
		states = self.s
		actions = self.a
		trans = np.zeros((len(states), len(actions), len(states)))
		rewards = np.full((len(self.a), len(self.states)), 0)
		edge_probabilites = []
		edge_action_labels = {}
		for curr_state in states: # how many chips you have now
			for action in actions: # action = # chips bet
				# if not possible, go to lose
				if action > curr_state:
					trans[(curr_state, action, 0 )] = 1
				else:
					# if betting 0 
					if action == 0:
						trans[(curr_state, action, curr_state)] = 1
					else:
						# if you win
						next_state =  min(action + curr_state, self.num_win_chips)
						trans[(curr_state, action, next_state)] = self.win_prob
						edge_probabilites.append((curr_state, next_state, self.win_prob))
						edge_action_labels[(curr_state, next_state)] = action
						# if you lose 
						trans[(curr_state, action, curr_state - action)] = 1 - self.win_prob
						edge_probabilites.append((curr_state, curr_state - action, 1 - self.win_prob))
						edge_action_labels[(curr_state, curr_state - action)] = action

		for action in actions:
			rewards[action, 0] = -10
			rewards[action, self.num_win_chips] = 10
		return rewards
	def Run(self):
		self.mdp.ValueIteration()
		self.mdp.BuildPolicy()
		self.mdp.Display(True)
		self.Display()

	def initDisplay(self):
		self.graph = nx.MultiDiGraph()
		self.graph.add_nodes_from(self.mdp.S)
		self.graph_pos = nx.circular_layout(self.graph)
		

	def getMoves(self):
		policy_mat = self.mdp.policy.transpose()
		policy = [0 for i in self.s]
		for i in range(len(policy)):
			policy[i] = np.argmax(policy_mat[i])
		print("best move at each state")
		print(policy)

		return policy

	def Display(self, showpolicy=True):
		labels = {}
		# pdb.set_trace()
		values = self.mdp.values.tolist()[0]
		node_colors = [0 for i in range(self.num_win_chips+1)]
		# create node labels
		for state in self.mdp.S:
			labels[state] = str(state) + " \n " + str(round(values[state],2))
			node_colors[state] = -1 * values[state] 
		# draw nodes
		nx.draw_networkx_nodes(self.graph, self.graph_pos,node_color=node_colors)
		nx.draw_networkx_labels(self.graph, self.graph_pos, labels=labels) #, labels = self.node_labels)

		# choose which edge to show
		edge_labels = None
		edge_colors = []
		if showpolicy:
			moves = self.getMoves()
			edge_list, edge_labels = [], {}
			for i, move in enumerate(moves):
				# if you win
				edge_list.append((i, i + move)) #initial state, state + move
				edge_labels[(i, i + move)] = move
				edge_colors.append('g')
				# if you lose
				edge_list.append((i, max(0, i - move))) #initial state, state + move
				edge_labels[(i, max(0, i - move))] = move
				edge_colors.append('r')
			self.graph.add_edges_from(edge_list)
			# edge_colors = 'r'
		else: # show probabilities
			self.graph.add_weighted_edges_from(self.edge_probabilites)
			for edge in self.graph.edges():
				# pdb.set_trace()
				edge_colors.append(self.edge_action_labels[edge])
			edge_labels = self.edge_action_labels
		
		nx.draw_networkx_edges(self.graph, self.graph_pos, edge_color=edge_colors)
		nx.draw_networkx_edge_labels(self.graph, self.graph_pos, edge_labels=edge_labels)
		plt.show()
		# TODO clear edges

if __name__ == "__main__":
	a =  GridWorldAgent()
	a.Run()





