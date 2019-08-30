import pyglet
import math
from game import board, physical_object

#def half_round(x):
#    """rounds a float to the nearest ODD half integer (i.e. 1/2, 3/2, etc)"""
#    return round(x+1/2) - 1/2

class pacsprite(physical_object.physical_object):

    def __init__(self, spawn_location, *args, **kwargs):
        super(pacsprite, self).__init__(*args, **kwargs)
        self.spawn_location = spawn_location
        self.universal_speed = 0.9
        self.respawn()
        self.valid_moves = []

    def fractional_coordinates(self):
        #returns the non-integer parts of the 'grid coordinates'. if (x,y) =(12,18)
        #and the grid size is 8, get output (0.5,0.25) etc.
        self.frac_y = self.y/self.board.grid_square_height - math.floor(self.y/self.board.grid_square_height)
        self.frac_x = self.x/self.board.grid_square_width - math.floor(self.x/self.board.grid_square_width)

    def respawn(self):
        self.speed_multiplier=1
        self.speed = self.speed_multiplier*self.universal_speed
        self.current_dir = [0,1]
        self.x, self.y = self.spawn_location[0], self.spawn_location[1]
        self.rotation = 0

    def update_valid_moves(self):
        self.speed = self.universal_speed*self.speed_multiplier
        self.determine_grid_location()
        self.fractional_coordinates()
        check = [[1,0], [-1,0], [0,1], [0,-1]]
        self.valid_moves = []
        for vec in check:
            try:
                if self.board.grid[self.grid_location[0] + vec[0], self.grid_location[1] + vec[1]] == 1:
                    self.valid_moves.append(vec)
            except IndexError:
                #must be in 'teleport zone' at edge of board. So can add the direction.
                    self.valid_moves.append(vec)
        #For smoothness, we must also make a move towards the CENTER of the current cell valid.
        #We don't compare to 0.5 because this allows 'wiggle room' which we don't want.
        if self.frac_y<0.5 - self.speed/(2*self.board.grid_square_height):
            if [1,0] not in self.valid_moves:
                self.valid_moves.append([1,0])
        elif self.frac_y>0.5 + self.speed/(2*self.board.grid_square_height):
            if [-1,0] not in self.valid_moves:
                self.valid_moves.append([-1,0])
        if self.frac_x<0.5 - self.speed/(2*self.board.grid_square_width):
            if [0,1] not in self.valid_moves:
                self.valid_moves.append([0,1])
        elif self.frac_x > 0.5 + self.speed/(2*self.board.grid_square_width):
            if [0,-1] not in self.valid_moves:
                self.valid_moves.append([0,-1])

    def teleport(self):
        #If the sprite is near the edge of the board (i.e. goes down the middle horrizonatal
        #in the original pacman game), then it teleports to the other side!
        if self.x < self.board.grid_square_width/8:
            self.x = self.board.size[1]-self.board.grid_square_width/8
        if self.x > self.board.size[1] - self.board.grid_square_width/8:
            self.x = self.board.grid_square_width/8
        if self.y < self.board.grid_square_height/8:
            self.y = self.board.size[0] - self.board.grid_square_height/8
        if self.y > self.board.size[0] - self.board.grid_square_height/8:
            self.y = self.board.grid_square_height/8

    def move(self, dir):
        self.update_valid_moves()
        if dir in self.valid_moves:
            if dir[0] == 0:
                self.x += dir[1]*self.speed
                self.y = (self.grid_location[0] + 1/2) * self.board.grid_square_height
            elif dir[1] == 0:
                self.y += dir[0]*self.speed
                self.x = (self.grid_location[1] + 1/2) * self.board.grid_square_width
        self.teleport()
