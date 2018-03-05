import pygame
import sys
import csv
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class PathConverter(object):
	def init(file_name, width=100, height = None):
		# default to square
		if not height:
			height = width

		self.data = self.read_data(file_name)
		pygame.init()
		 
		# Set the width and height of the screen [width, height]
		screen = pygame.display.set_mode((width, height))
		 
		pygame.display.set_caption("My Game")
		 
		# Loop until the user clicks the close button.
		done = False
		 
		# Used to manage how fast the screen updates
		clock = pygame.time.Clock()
	 
		# -------- Main Program Loop -----------
		while not done:
		    # --- Main event loop
		    for event in pygame.event.get():
		        if event.type == pygame.QUIT:
		            done = True
		 	
		    # --- Game logic should go here
		 
		    # --- Screen-clearing code goes here
		 
		    # Here, we clear the screen to white. Don't put other drawing commands
		    # above this, or they will be erased with this command.
		 
		    # If you want a background image, replace this clear with blit'ing the
		    # background image.
		    screen.fill(WHITE)
		 
		    # --- Drawing code should go here
		 
		    # --- Go ahead and update the screen with what we've drawn.
		    pygame.display.flip()
		 
		    # --- Limit to 60 frames per second
		    clock.tick(60)
		 
		# Close the window and quit.
		pygame.quit()

	def read_data(self, file_name):
		with open(file_name) as csvfile:
			reader = csv.reader(csvfile)
		return reader





if __name__ == "__main__":
	c = PathConverter(width = 1000, file_name = "path.csv")
	init()