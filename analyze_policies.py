from gridworld_agent import *
from reward_guesser import *
import csv
import os
import json
import sys
import pdb

def to_csv(d, old_filename):
    new_filename = os.path.join(paths_output_dirname, old_filename)
    with open(new_filename, 'w+') as f:
        for key in d:
            # start state, probability  at each state
            f.write("%s,%s\n"%(key,','.join(map(str, d[key]))))
# no I don't super remember what this function does, not used
# def process(filename):
#     b = GridWorldAgent(width=sizeworld,height=sizeworld,rewardValues =  {1:10}, softmax=0.2)
#     with open(os.path.join(paths_dirname, filename)) as csvfile:
#         reader = csv.reader(csvfile)
#         data = list(reader)
#     print(filename)
#     data = [(int(x),int(y)) for (x,y) in data]
#     action_list, path_list = b.takeListGetPath(data)
#     guesser = RewardGuesser(policies_dirname, action_list, path_list, sizeworld)
#     # this returns a dict for each csv, key from 0 to w * h, val is list from of probabilities
#     res = guesser.getMarginalProb()
#     to_csv(res, filename)
#     return res

def np_to_csv(d, old_filename):
    new_filename = os.path.join(paths_output_dirname, old_filename)
    numpy.savetxt("new_filename" + ".csv", d, delimiter=",")


    # I am just writing out what should happen
def get_prob_goal_directed(filename):
    """
    so i have a list of actions and a dimension for gridworld
    what I want is to first get a list of start locations where the action list could happen in that world
    I do that by randomly sampling a start location and retrying when I hit an edge
    - there, I want to know the number of tries it took to get X succsesful starts, and where those starts are
    so if I have 50 action list and start locations
    for each of those lists, I need to run reward guesser on them, using the np arrays
    and average all those values 
    """
    print("Processing %s" % filename)
    b = GridWorldAgent(width=worldwidth,height=worldwidth,rewardValues =  {1:10}, softmax=0.2, diagonal=diag)
    with open(os.path.join(actionlistdirectory, filename)) as f:
        l = f.readline()
        action_list = [int(x) for x in l.split(',')]
    state_list = b.takeActionListGetStateList(action_list, 60, 60)
   
    guesser = RewardGuesser(policies_dirname, action_list, state_list, worldwidth**2, diagonal=diag)
    # nope- here, I want the guesser to just give me the marginal prob
    res = guesser.genForCSV()
    np_to_csv(res, filename)




if __name__ == '__main__':
    if len(sys.argv) < 6:
        print("usage: python analyze_policies [actionlistdirectory] [policiesdirectory] [worldwidth] [-d]")
        exit(1)
    global actionlistdirectory
    actionlistdirectory = sys.argv[1]
    global policies_dirname
    policies_dirname = sys.argv[2]
    global worldwidth
    worldwidth = int(sys.argv[3])
    numsamples = int(sys.argv[4])
    global diag
    if len(sys.argv) == 7 and sys.argv[6] == "-d":
        diag = True
    else:
        diag = False 

    # make directory for output results
    global paths_output_dirname
    paths_output_dirname = os.path.basename(os.path.normpath(actionlistdirectory)) + "_results"
    if not os.path.exists(paths_output_dirname):
        os.makedirs(paths_output_dirname)
    for filename in os.listdir(actionlistdirectory):
        # if filename.startswith(letter):
	if not os.path.isfile(os.path.join(paths_output_dirname, filename)):
		get_prob_goal_directed(filename)
