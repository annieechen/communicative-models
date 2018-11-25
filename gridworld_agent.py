import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from math import log

from itertools import product

from mdp import MDP 
from map import Map
import pdb
import random

class GridWorldAgent(object):
    def __init__(self, softmax=0.01, rewardWhenReached=False, width=10,height=None, diagonal=False, rewardValues=None,):
        """
        This class stores the values for the gridworld, and allows for creating paths/visualizing 

        Args:
            rewardWhenReached (bool): if true, creates reward matrix so reward when in state. Else, when enters state
            width, height(bool): size of gridworld (to be passed to map)
            diagonal (bool): whether agents can travel diagonally 
            rewardValues (dict): (x,y) tuples to values of squares, passed to _CreateRewards
            s (list): List of states.
            a (list): List of actions available.
            rewardLocations(dict): list of coordinates(1 indexed) with rewards <- should be same as reward values
            diagonal (boolean): Determines if agents can travel diagonally.
            t (matrix): Transition matrix. T[SO,A,SF] contains the probability that agent will go from SO to SF after taking action A.
            policy_moves(list): move to take in each state given maxing
        """
        self.map = Map(diagonal=True)
        # fill states, transition, actions
        self.width = width
        if height == None:
            self.height = width
        else:
            self.height = height
        self.s, self.t, self.a = self.map.BuildGridWorld(self.width, self.height, diagonal)

        self.rewardWhenReached = rewardWhenReached
        self.rewardLocations = None
        self.r = self._CreateRewards(rewardValues)
        self.mdp = MDP(self.s,self.a,self.t,self.r, tau =softmax)
        # self.policy_moves = None
        self.policy = None
        # pdb.set_trace()
        self.hasRun = False
        if not self.mdp.Validate():
            raise AssertionError

    def _CreateRewards(self, rewardValues=False, display=False):
        """
        valsDict (dictionary): maps (x,y) to reward of state
        """
        # initialize to default
        if not rewardValues:
            rewardValues = {(1,1):10, (self.width,self.height): -10}
        self.rewardLocations = rewardValues
        rewards = np.full((len(self.a), len(self.s)), -1)
        # transform coordinates to states
        stateRewards = {}
        for coord, val in rewardValues.iteritems():
            if type(coord) is int:
                state = coord
            else:
                state = self.map.GetRawStateNumber(coord)
            if display:
                print("coord: " + str(coord) + " state: " + str(state) + " val: " + str(val))
            stateRewards[state] = val
        # loop through all states and actions, if they reach a reward, set it
        if self.rewardWhenReached:
            for curr_state in self.s: 
                for action in self.a: 
                    next_state = self.map.makeMove(curr_state, action)
                    if next_state in stateRewards:
                        rewards[action, curr_state] += stateRewards[next_state]
        # any action they take in reward state = reward
        else:
            for state, val in stateRewards.iteritems():
                for action in self.a:
                    rewards[action, state] += val

        # alter transition matrix so that after they enter reward state, enter dead state
        for state, val in stateRewards.iteritems():
            # 0 everything out first
            self.t[state, :, :] = 0
            # now 100% chance will move to dead state
            self.t[state,:, len(self.s) - 1] = 1
        
        return rewards

    def Run(self, display=False, get_moves =False):
        self.mdp.ValueIteration()
        self.mdp.BuildPolicy()
        if get_moves:
            self.getMoves()
        if display:
            self.Display()
        self.hasRun = True
        

    # get list of best moves at each state
    def getMoves(self, print_moves = True):
        # check to make sure ValueIteration and BuildPolicy are called
        if not np.any(self.mdp.values):
            self.mdp.ValueIteration()
        if not np.any(self.mdp.policy):
            self.mdp.BuildPolicy()
        policy_mat = self.mdp.policy.transpose()
        policy = [0 for i in self.s]
        for i in range(len(policy)):
            policy[i] = np.argmax(policy_mat[i])
        if print_moves:
            print("best move at each state")
            policy_names = self.map.GetActionNames(policy)
            # pdb.set_trace()
            print(policy_names[:-1].reshape((self.height, self.width)))
        self.policy = policy
        return policy


    def Display(self, showpolicy=False, path_list=None):
        data = self.mdp.values[:,:-1].reshape((self.height, self.width))
        fig, ax = plt.subplots()
        ax.matshow(data, cmap='Greens')
        """
        this wasn't tested after I changed the index for the coordinates, may not work
        if showpolicy:
            for (y, x), z in np.ndenumerate(data):
                if (x + 1, y + 1,) in path_list:
                    ax.annotate( '{:0.1f}'.format(z), xy=(x , y), xycoords='data', backgroundcolor='purple')
                else:
                    ax.annotate( '{:0.1f}'.format(z), xy=(x , y), xycoords='data')
        """
        # don't change colors
        for (y, x), z in np.ndenumerate(data):
            ax.annotate( '{:0.1f}'.format(z), xy=(x , y), xycoords='data')#, ha='right', va='top')
        # highlight reward values
        for state, val in self.rewardLocations.iteritems():
            if type(state) is int:
                x,y = self.map.GetCoordinates(state)
            else:
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
        state_path_list = []
        coord_path_list = []
        action_list = []
        while num_steps < max_path_length:
            # move to next state
            best_action = self.policy[curr_state]
            state_path_list.append(curr_state)
            coord_path_list.append(self.map.GetCoordinates(curr_state))
            action_list.append(best_action)
            curr_state = self.map.makeMove(curr_state, best_action)
            num_steps += 1
        if print_path:
            print("path from " + str(start_coordinates))
            for i in range(max_path_length):
                print(str(coord_path_list[i]) + str(self.map.GetActionName(action_list[i])))
            self.Display(showpolicy = True, path_list = coord_path_list)
        return action_list, coord_path_list, state_path_list

    # should also be deprecated, I think I shouldnt need the raw state number to to do this
    def takeListGetPath(self, x_y_list):
        state_list = []
        action_list = []
        curr_x, curr_y = x_y_list[0]
        # ["L", "R", "U", "D"]
        for x,y in x_y_list[1:]:
            past_x, past_y = curr_x,curr_y
            curr_x, curr_y = x,y
            # if DR
            # if x > past_x and y > past_y:
            #     action_list.append(7)
            # # DL
            # elif x < past_x and y > past_y:
            #     action_list.append(6)
            # # UR
            # elif x > past_x and y < past_y:
            #     action_list.append(5)
            # # UL
            # elif x < past_x and y < past_y:
            #     action_list.append(4)
            # else:
            # if down
            if y > past_y:
                action_list.append(3)
            # up
            if y < past_y:
                action_list.append(2)
            # R
            if x > past_x:
                action_list.append(1)
            # L
            if x < past_x:
                action_list.append(0)
            state_list.append(self.map.GetRawStateNumber((x,y)))
            if len(action_list) != len(state_list):
                print(x,y,past_x, past_y)
        return action_list, state_list

    def takeStateListGetCoordList(self, state_list, includeStartState=True):
        coord_list = []
        if includeStartState:
            x, y = self.getMiddleOfMap()
            coord_list.append([x,y])
        for state in state_list:
            x, y = self.map.GetCoordinates(state)
            coord_list.append([x,y])
        return coord_list

    def takeActionListGetStateList(self, action_list, start_x, start_y):
        state_list = []
        # this should be fine without extra check for diagonals, 
        # bc if there no diagonals in the list then they won't map in
        action_map = ["L", "R", "U", "D", "UL", "UR", "DL", "DR"]
        curr_x, curr_y = start_x, start_y
        for action_num in action_list:
            action = action_map[action_num]
            if 'L' in action:
                next_x = curr_x - 1
            if 'R' in action:
                next_x = curr_x + 1
            if 'U' in action:
                next_y = curr_y - 1
            if 'D' in action:
                next_y = curr_y + 1
            # now check if out of bounds
            if next_x < 0 or next_x == self.width or next_y < 0 or next_y == self.height:
                return
            # else, this move works, add curr_x curr_y
            state_list.append(self.map.GetRawStateNumber((curr_x, curr_y)))
            curr_x, curr_y = next_x, next_y
        return state_list


   

    # generates all paths of length n
    # returns list of (action_list, state_list) tupics
    def genAllPaths(self, n):
        action_map = ["L", "R", "U", "D"]#, "UL", "UR", "DL", "DR"]
        action_lists = product(range(4), repeat=n)
        results = []
        for actions in action_lists:
            action_list, state_list = [], []
            i = 0
            curr_x, curr_y = self.getMiddleOfMap()
            for action_num in actions:
                action = action_map[action_num]
                past_x, past_y = curr_x, curr_y

                if 'L' in action:
                    curr_x -= 1
                if 'R' in action:
                    curr_x += 1
                if 'U' in action:
                    curr_y -= 1
                if 'D' in action:
                    curr_y += 1

                if curr_x < 0 or curr_x >= self.width or curr_y < 0 or curr_y >= self.height:
                    # print("SHOULD NOT HAPPEN")
                    break
                state_list.append(self.map.GetRawStateNumber((curr_x, curr_y)))
                action_list.append(action_num)
                i += 1
            # only append full paths that didn't hit an edge
            # if len(action_list) == len(actions):
            results.append((action_list, state_list))
        return results


    def getMiddleOfMap(self):
        return self.width//2, self.height//2

    def getLikelihoodOfPath(self, action_list, path_list):
        if not self.hasRun:
            self.Run()
        probabilities = self.mdp.policy
        prob_list = []
        product_probabilities = 1
        for i in range(len(action_list)):
            action, state = action_list[i], path_list[i]
            product_probabilities *= (probabilities[action,state])
            # print(state)
            if state in self.rewardLocations and len(self.rewardLocations) == 1:
            	# print("found reward, stopped counting")
            	break
        return product_probabilities


    def getLikelihoodAllPaths(self, lengthofPath, display=False, topthree=False):
    	results = self.genAllPaths(lengthofPath)

        coordAndLikelihood = []
        for path in results:
            action_list, state_list = path
            likelihood = self.getLikelihoodOfPath(action_list, state_list)
            coord_list = self.takeStateListGetCoordList(state_list)
            coordAndLikelihood.append((np.array(coord_list), likelihood))
        if display:
        	self.displayAllPaths(coordAndLikelihood, topthree=topthree)
        return coordAndLikelihood
    def displayAllPaths(self, coordAndLikelihood, topthree=False):
        # sort list so paths with highest likelihood are last
        coordAndLikelihood.sort(key = lambda x:x[1])

        data = np.zeros((self.height, self.width))
        # highlight reward values
        for state, val in self.rewardLocations.iteritems():
            if type(state) is int:
                x,y = self.map.GetCoordinates(state)
            else:
                x,y = state
            data[y][x] = val
        # highlight start
        start_x, start_y = self.getMiddleOfMap()
        #coordAndLikelihood[0][0][0]
        # print((start_x, start_y))
        data[start_y][start_x] = -10

        fig, ax = plt.subplots()
        ax.matshow(data, cmap='Greens')

        # each path
        if topthree:
        	coordAndLikelihood = coordAndLikelihood[0:3] + coordAndLikelihood[-3:]
        	# print(coordAndLikelihood)
        logged_likelihoods = [-1 * log(i[1]) for i in coordAndLikelihood]
        logged_color_list = [float(i)/max(logged_likelihoods) for i in logged_likelihoods]
        normal_color_list = [float(i[1])/(max(coordAndLikelihood, key=lambda x:x[1])[1]) for i in coordAndLikelihood]
        colors = plt.get_cmap('viridis')
        for idx, item in enumerate(coordAndLikelihood):
            path, _ = item
            plt.plot(path[:, 0], path[:, 1], color=colors(logged_color_list[idx]), linewidth=7.0)
            plt.plot(path[:, 0], path[:, 1], color=colors(normal_color_list[idx]), linewidth=1.0)
        plt.show()

if __name__ == "__main__":
    a =  GridWorldAgent(width=3,height=4, rewardValues = {(2,4):10, (3,1): -20})
    a.Run(display = True)





