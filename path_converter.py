import pygame
import sys
import csv
from collections import OrderedDict
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class PathConverter(object):
    def __init__(self, file_name, width=100, height = None, scale = 10):
        # default to square
        if not height:
            height = width
        self.h = height
        self.w = width
        self.scale = scale
        self.file_name = file_name
        self.raw_data = self.read_data(file_name)
        # data is always a list of [(x,y)] coordinates



    def convert(self, remove_duplicates=True):
        scaled = self.scale_data(self.raw_data)
        if remove_duplicates:  
            scaled = self.remove_duplicates(scaled)
        self.write_data_to_file(scaled)
            def read_data(self, file_name):
        with open(file_name) as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
        data = [(float(x),float(y)) for (x,y) in data]
        return data


    # just turns from strings to nums
    def scale_data(self, data):
        s = float(self.scale)
        final = [None] * len(data)
        for i in range(len(data)):
            x,y = data[i]
            final[i] = [round(x/s), round(y/s)]
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


    def data_to_rects(self, data, scale = False):
        s = self.scale
        if scale:
            rects = [[x*s, y*s, s,s] for (x,y) in data]
        else:
            rects = [[x,y,1,1] for (x,y) in data]
        return rects

    def write_data_to_file(self, data, file_name=None):
        # default filename
        if not file_name:
            file_name = "scaled" + self.file_name 
        with open(file_name, 'w+') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print("finished writing to " + file_name)

    def visualize(self, data):

        rects = self.data_to_rects(data)
        pygame.init()
         
        # Set the width and height of the screen [width, height]
        screen = pygame.display.set_mode((self.w, self.h))
         
        pygame.display.set_caption("My Game")
         
        # Loop until the user clicks the close button.
        done = False
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        curr_square = None
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
            
            # --- Game logic should go here
         
            # --- Screen-clearing code goes here
         
            # Here, we clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.
         
            # If you want a background image, replace this clear with blit'ing the
            # background image.
            screen.fill(BLACK)
         
            # --- Drawing code should go here
            if past_square:
                pygame.draw.rect(screen, RED, past_square)
            pygame.draw.rect(screen, GREEN, curr_square)
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
         
            # --- Limit to 60 frames per second
            clock.tick(40)
         
        # Close the window and quit.
        pygame.quit()




    def get_both(self, data):
        return self.data_to_rects(self.convert_data(data), scale=True)
        # self.data_to_rects(data) + self.data_to_rects(self.convert_data(data), scale=True)


if __name__ == "__main__":
    c = PathConverter(file_name = "path.csv", width = 1000)
    c.convert()