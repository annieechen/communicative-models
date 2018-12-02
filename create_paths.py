import csv
import pdb

ActionNames = ["L", "R", "U", "D", "UL", "UR", "DL", "DR"]

## path makeups

A = ['R','R','R','R','R']
B = ['L','L','L','L','L']
C = ['L','U','U','U','U']
D = ['D','D','D','D','D']

E = ['UR','UR','UR','UR','UR']
F = ['DR','DR','DR','DR','DR']
G = ['UL','UL','UL','UL','UL']
H = ['DL','DL','DL','DL','DL']


I = ['R','R','UR','U','U']
J = ['R','R','DR','D','D']
K = ['L','L','UL','U','U']
L = ['L','L','DL','D','D']


M = ['U','U','UR','R','R']
N = ['D','D','DR','R','R']
O = ['U','U','UL','L','L']
P = ['D','D','DL','L','L']


PARTS = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P]

paths = [None] *23


paths[0] = "akdo" # BeenHereBeforeButNotHome, middle, bottom
paths[1] = "akil" # BeenHereBeforeButNotHome, left, bottom
paths[2] = "ibli" # BeenHereBeforeButNotHome, middle, bottom
paths[3] = "aaaa" # Maximally efficient  left, middle
paths[5] = "ebjn" # NotOneDirection middle, middle
paths[4] = "eeee" # Maximally efficient left, bottom
paths[6] = "iffa" # NotOneDirection middle, left
paths[7] = "indd" # NotOneDirection left, middle
paths[8] = "aeea" # OneDirection left, bottom
paths[9] = "iaci" # OneDirection
paths[10] = "iacm" # OneDirection
paths[11] = "inpi" # OneInversion
paths[12] = "ipan" # OneInversion
paths[13] = "ipff" # OneInversion
paths[14] = "eaea" # Repeat, no home, no inversion, no intersection
paths[15] = "ifif" # Repeat, no home, no inversion, no intersection
paths[16] = "inin" # Repeat, no home, no inversion, no intersection
paths[17] = "abkj" # ReturnsHome
paths[18] = "ibla" # ReturnsHome
paths[19] = "ihpe" # ReturnsHome
paths[20] = "ebah" # ReturnsHomeSymmetrically
paths[21] = "ifgp" # ReturnsHomeSymmetrically
paths[22] = "ihep" # ReturnsHomeSymmetrically
# paths[23] = "eaaa" #Warm-up1
# paths[24] = "inol" #Warm-up2
# paths[25] = "aagd" #Warm-up3
# paths[26] = "aain" #Warm-up4

test = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm','n', 'o', 'p']

# LENGTH = 21

# def remove_third(l):
# 	return l[0:1] + l[3:4] + l[6:7]


for path in paths:
	action_list = []
	for c in path:
		part_index = ord(c) - 97
		action_list += PARTS[part_index]
	action_indexes = []
	for action in action_list:
		action_indexes.append(ActionNames.index(action))

	with open("generated_action_lists_len25_d/"+path, 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(action_indexes)
		print("finished writing to " + path)

	# print("%s %i %i | %i %i" % (path, min_h, min_v, max_h, max_v))

	# now have a whole action list, write to file
	# with open(os.path.join("standard_data", paths + ".csv")):







