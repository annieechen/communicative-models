from mdp import MDP 
import numpy as np
import pdb


WINNING_PROB = 0.5
NUM_WIN_CHIPS = 5

class BettingAgent(object):
	def __init__(self, win_prob=WINNING_PROB,  num_win_chips = NUM_WIN_CHIPS):
		s,a,t,r = self._CreateParams(win_prob, num_win_chips)
		self.mdp = MDP(s,a, t,r)
		if not self.mdp.Validate():
			raise AssertionError

	def _CreateParams(self, win_prob, num_win_chips):
		states = list(range(0, num_win_chips + 1)) 
		actions = list(range(0, num_win_chips + 1)) 
		trans = np.zeros((len(states), len(actions), len(states)))
		rewards = np.zeros((len(actions), len(states)))
		for curr_state in states: # how many chips you have now
			for action in actions: # action = # chips bet
				# for next_state in states: # how many chips you have if you win
				# 	# set everything to 0 first
				# 	trans[(curr_state, action, next_state)] = 0
				# now set the probabilities the actions lead to
				# if not possible, go to lose
				if action > curr_state:
					trans[(curr_state, action, 0 )] = 1
				else:
					# if betting 0 
					if action == 0:
						trans[(curr_state, action, curr_state)] = 1
					else:
						# if you win
						trans[(curr_state, action, min(action + curr_state, num_win_chips))] = win_prob
						# if you lose 
						trans[(curr_state, action, curr_state - action)] = 1 - win_prob

		for action in actions:
			rewards[action, 0] = -10
			rewards[action, NUM_WIN_CHIPS] = 10
		return states, actions, trans, rewards

	def Run(self):
		self.mdp.ValueIteration()
		# self.mdp.BuildPolicy()
		pdb.set_trace()
		self.mdp.Display(True)

if __name__ == "__main__":
	a =  BettingAgent()
	a.Run()





