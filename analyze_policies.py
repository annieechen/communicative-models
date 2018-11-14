from gridworld_agent import *
from reward_guesser import *
import csv
import os
import json
import sys

def to_csv(d, old_filename):
    new_filename = os.path.join(paths_output_dirname, old_filename)
    with open(new_filename, 'w+') as f:
        writer = csv.writer(f, delimiter=',')
        for key in d:
            l = d[key]
            writer.writerow(l)
# no I don't super remember what this function does
def process(filename):
    b = GridWorldAgent(width=35,height=35,rewardValues =  {1:10}, softmax=0.2)
    with open(os.path.join(paths_dirname, filename)) as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    print(filename)
    data = [(int(x),int(y)) for (x,y) in data]
    action_list, path_list = b.takeListGetPath(data)
    guesser = RewardGuesser(policies_dirname, action_list, path_list, sizeworld)
    # this returns a dict for each csv, key from 0 to w * h, val is list from of probabilities
    res = guesser.getMarginalProb()
    to_csv(res, filename)
    return res



if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("usage: python analyze_policies [pathsdirectory] [policiesdirectory] [sizeworld]")
        exit(1)
    global paths_dirname
    paths_dirname = sys.argv[1]
    global policies_dirname
    policies_dirname = sys.argv[2]
    global sizeworld
    sizeworld = int(sys.argv[3])
    # make directory for output results
    global paths_output_dirname
    paths_output_dirname = paths_dirname + "_results"
    if not os.path.exists(paths_output_dirname):
        os.makedirs(paths_output_dirname)
    for filename in os.listdir(paths_dirname):
        # if filename.startswith(letter):
        process(filename)