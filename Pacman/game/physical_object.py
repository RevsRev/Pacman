import pyglet
import math
from game import board

class physical_object(pyglet.sprite.Sprite):
    def __init__(self, board, *args, **kwargs):
        super(physical_object, self).__init__(*args, **kwargs)
        self.board = board
        self.determine_grid_location()
        self.y = (self.grid_location[0] + 1/2) * self.board.grid_square_height
        self.x = (self.grid_location[1] + 1/2) * self.board.grid_square_width
        self.valid_moves = []
        self.counter = 0
        self.count_limit = 480

    def determine_grid_location(self):
        self.grid_location = [math.floor(self.y/self.board.grid_square_height),
            math.floor(self.x/self.board.grid_square_width)]

    def collides_with(self, other_obj):
        #For the purposes of pacman, we say that two objects collide if they occupy
        #the same grid square.
        if self.grid_location[0] == other_obj.grid_location[0] \
        and self.grid_location[1] == other_obj.grid_location[1]:
            return True
        else:
            return False

    def delete(self):
        super(physical_object,self).delete()
