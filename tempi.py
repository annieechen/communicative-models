from gridworld_agent import *
from reward_guesser import *
import csv
import os
import json

b = GridWorldAgent(width=32,height=32,rewardValues =  {1:10})


results = {}
for filename in os.listdir("scaled_data"):
	if filename.startswith('i')
    with open(os.path.join("scaled_data", filename)) as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    data = [(int(x),int(y)) for (x,y) in data]
    action_list, path_list = b.takeListGetPath(data)
    c = RewardGuesser(b.map.T, b.map.S, b.r, action_list, path_list, 32,32)
    res = c.getMarginalProb()
    results[filename] = (res, len(action_list))


with open("finalresultsi", 'w+') as f:
    f.write(json.dumps(results))