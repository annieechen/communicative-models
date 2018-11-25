import pygame
import sys
import csv
import os
from collections import OrderedDict

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class PathConverter(object):
    def __init__(self, file_name, scale, include_diagonals):
        self.scale = scale
        self.file_name = file_name
        self.raw_data = self.read_data(file_name)
        self.include_diagonals= include_diagonals
        # data is always a list of [(x,y)] coordinates

    def convert(self, remove_duplicates=True, write_data=True):
        scaled = self.scale_data(self.raw_data)
        if remove_duplicates:
            scaled = self.remove_duplicates(scaled)
            # scaled = self.replace_with_diagonals(scaled)
        if not self.include_diagonals:
            scaled = self.remove_diagonals(scaled)
        action_list = self.convert_coordstates_to_actions(scaled)
        if write_data:
            self.write_data_to_file(action_list)

    def read_data(self, file_name):
        with open(file_name) as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)[1:]
        data = [(float(x),float(y)) for (x,y) in data]
        return data


    # just turns from strings to nums
    def scale_data(self, data, remove_extra=False):
        s = float(self.scale)
        final = [None] * len(data)
        for i in range(len(data)):
            x,y = data[i]
            final[i] = [round(x/s), round(y/s)]
        if remove_extra:
            min_x = min(final, key= lambda t: t[0])[0] - 1
            min_y = min(final, key= lambda t: t[1])[1] - 1
            final = [(int(x - min_x), int(y - min_y)) for (x,y) in final]

        return final

    def remove_duplicates(self, data):
        final = []
        curr = None
        for row in data:
            prev = curr
            curr = row
            if prev == curr:
                continue
            final.append(curr)
        return final

    def remove_diagonals(self, data):
    	final = []
    	prev_dir = 0
        curr_x, curr_y = data[0]
        for x,y in data[1:]:
            past_x, past_y = curr_x, curr_y
            curr_x, curr_y = x,y
            # if this is a diagonal
            if curr_x != past_x and curr_y != past_y:
            	# do vertical first, then horizontal
            	print("removed diagonal")
            	final.append((past_x, curr_y))
            	final.append((curr_x, curr_y))
            else:
            	final.append((curr_x, curr_y))
        return final


    def convert_coordstates_to_actions(self, coordlist):
        action_list = []
        curr_x, curr_y = coordlist[0]
        # ["L", "R", "U", "D"]
        for x,y in coordlist[1:]:
            past_x, past_y = curr_x,curr_y
            curr_x, curr_y = x,y
            if self.nclude_diagonals:
                #if DR
                if x > past_x and y > past_y:
                    action_list.append(7)
                    continue
                # DL
                elif x < past_x and y > past_y:
                    action_list.append(6)
                    continue
                # UR
                elif x > past_x and y < past_y:
                    action_list.append(5)
                    continue
                # UL
                elif x < past_x and y < past_y:
                    action_list.append(4)
                    continue
            # L
            if x < past_x:
                action_list.append(0)
            # R
            if x > past_x:
                action_list.append(1)
            # up
            if y < past_y:
                action_list.append(2)
            # down
            if y > past_y:
                action_list.append(3)
        return action_list

    """
    Currently deprecated, because I'm not testing the version with diagnoals
    nything that becomes up down and left right becomes diagonal
    # must have called remove duplicates
    """
    def replace_with_diagonals(self, data):

        final = []
        # None, 2 for vert, 3 for horizontal
        prev_dir = 0
        curr_x, curr_y = data[0]
        for x,y in data[1:]:
            past_x, past_y = curr_x, curr_y
            curr_x, curr_y = x,y
            # pdb.set_trace()
            if curr_x == past_x:
                curr_dir = 2
            elif curr_y == past_y:
                curr_dir = 3
            if curr_dir * prev_dir == 6:
                del final[-1]
                prev_dir = 0
            else:
                prev_dir = curr_dir
            final.append((curr_x, curr_y))
        return final

    def data_to_rects(self, data, scale = False):
        s = self.scale
        if scale:
            rects = [[x*s, y*s, s,s] for (x,y) in data]
        else:
            rects = [[x,y,10,10] for (x,y) in data]
        return rects

    def write_data_to_file(self, data, file_prefix=None):
        # default filename
        if file_prefix:
            file_name =  file_prefix + self.file_name
        else:
            file_name = self.file_name
        with open(os.path.join(outputdirectory, os.path.basename(file_name)), 'w+') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print("finished writing to " + file_name)
        max_x = str(max(data, key = lambda t: t[0])[0])
        max_y = str(max(data, key = lambda t: t[1])[1])  
        print("max (x,y) = " + max_x + "," + max_y)

    def visualize(self, data = None):
        if not data:
            data = self.raw_data
        rects = self.data_to_rects(data, scale=True)
        pygame.init()
         
        # Set the width and height of the screen [width, height]
        screen = pygame.display.set_mode((self.w, self.h))
         
        pygame.display.set_caption("My Game")
         
        # Loop until the user clicks the close button.
        done = False
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        curr_square = None
        screen.fill(BLACK)
        # -------- Main Program Loop -----------
        for row in rects:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            past_square = curr_square
            curr_square = row
            if curr_square == past_square:
                continue
            print(curr_square)

            if past_square:
                pygame.draw.rect(screen, RED, past_square)
            pygame.draw.rect(screen, GREEN, curr_square)
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            # --- Limit to 60 frames per second
            clock.tick(5)
         
        # Close the window and quit.
        # pygame.quit()

    def get_both(self, data):
        return self.data_to_rects(self.convert_data(data), scale=True)
        # self.data_to_rects(data) + self.data_to_rects(self.convert_data(data), scale=True)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: path_converter [datainputdirectory] [actionlistresultsdirectory] [scalefactor] [-d if diagnoals")
        exit(1)
    datainputdirectory = sys.argv[1]
    scalefactor = sys.argv[2]
    # this one is a global so write_data_to_file can use it
    global outputdirectory
    outputdirectory = sys.argv[3]
    if len(sys.argv) == 5 and sys.argv[4] == "-d":
        include_diagonals = True
    else:
        include_diagonals = False

    for file in os.listdir(datainputdirectory):
        print ("Processing %s" % file)
        c = PathConverter(file_name=os.path.join(datainputdirectory, file),scale=scalefactor, include_diagonals=include_diagonals)
        c.convert()
