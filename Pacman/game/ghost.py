import pyglet
import math
import random
from game import pacsprite, resources

class ghost(pacsprite.pacsprite):

    def __init__(self, ghost_type, wave_mode = "scatter", *args, **kwargs):
        super(ghost, self).__init__(*args, **kwargs)
        self.initiate_type(ghost_type)
        self.wave_mode = wave_mode
        self.frightened = False

    def switch_wave_mode(self):
        if self.wave_mode == "scatter":
            if self.movement_mode == "scatter":
                self.init_movement_mode("chase")
            self.wave_mode = "chase"
        else:
            if self.movement_mode == "chase":
                self.init_movement_mode("scatter")
            self.wave_mode = "scatter"

    def initiate_type(self,ghost_type):
        self.ghost_type = ghost_type
        self.ghost_state = 0
        self.dot_counter = 0
        if ghost_type == "blinky":
            self.ghost_states = resources.blinky_states
            self.grid_target = [35,33]
            self.init_movement_mode("chase")
            self.dot_limit = 0
            self.current_dir = [0,1]
        elif ghost_type == "pinky":
            self.ghost_states = resources.pinky_states
            self.grid_target = [35,2]
            self.init_movement_mode("stay_in_house")
            self.dot_limit = 0
            self.current_dir = [-1,0]
        elif ghost_type == "clyde":
            self.ghost_states = resources.clyde_states
            self.grid_target = [0,0]
            self.init_movement_mode("stay_in_house")
            self.dot_limit = 60
            self.current_dir = [1,0]
        elif ghost_type == "inky":
            self.ghost_states = resources.inky_states
            self.grid_target = [0,35]
            self.init_movement_mode("stay_in_house")
            self.dot_limit = 30
            self.current_dir = [1,0]

    def stay_in_house(self):
        if self.dot_counter >= self.dot_limit:
            self.init_movement_mode("moving_out")
        else:
            if self.ghost_type != "blinky":
                if self.current_dir == [-1,0]:
                    if self.y > self.board.grid_square_height*17.5:
                        self.y -= self.speed
                    else:
                        self.current_dir = [1,0]
                else:
                    if self.y < self.board.grid_square_height*19.5:
                        self.y += self.speed
                    else:
                        self.current_dir = [-1,0]

    def init_movement_mode(self, mode):
        self.movement_mode = mode
        self.ghost_state = 0
        if mode == "chase":
            self.speed_multiplier = 1
            self.frightened = False
        elif mode == "scatter":
            self.current_dir = [0-self.current_dir[0], 0-self.current_dir[1]]
            self.speed_multiplier = 1
            self.frightened =False
        elif mode == "frightened":
            self.frightened = True
            self.current_dir = [0-self.current_dir[0], 0-self.current_dir[1]]
            self.speed_multiplier = 0.5
        elif mode == "dead":
            self.frightened = False
            self.speed_multiplier = 2
            self.target = [21,13]
            self.closest_move_to_target()
        elif mode == "moving_in":
            self.speed_multiplier = 1
            self.speed = self.speed_multiplier * self.universal_speed
            self.current_dir = [-1,0]
        elif mode == "stay_in_house":
            self.speed_multiplier = 1
            self.speed = self.speed_multiplier * self.universal_speed
            self.dot_counter = 0
        elif mode == "moving_out":
            self.speed_multiplier = 1
            self.speed = self.speed_multiplier * self.universal_speed
            self.current_dir = [1,0]

    def get_target(self, Pacman, other_ghost = None):
        if self.movement_mode == "chase":
            if self.ghost_type == "blinky":
                self.target = Pacman.grid_location
            elif self.ghost_type == "pinky":
                self.target = [Pacman.grid_location[0] + Pacman.current_dir[0]*4,
                    Pacman.grid_location[1] + Pacman.current_dir[1]*4]
            elif self.ghost_type == "clyde":
                if ghost.distance(self.grid_location, Pacman.grid_location)>8:
                    self.target = Pacman.grid_location
                else:
                    self.target = self.grid_target
            elif self.ghost_type == "inky":
                target = [2*Pacman.grid_location[0]+4*Pacman.current_dir[0] - other_ghost.grid_location[0],
                    2*Pacman.grid_location[1]+4*Pacman.current_dir[1]-other_ghost.grid_location[1]]
                if target[0] > self.board.grid.shape[0]:
                    target[0] = self.board.grid.shape[0]
                if target[1]> self.board.grid.shape[1]:
                    target[1] = self.board.grid.shape[1]
                self.target = target
        elif self.movement_mode == "scatter":
            self.target = self.grid_target
        elif self.movement_mode == "dead":
            self.target = [21,13]
        else:
            self.target = "none"

    def distance(loc_1, loc_2):
        #determines distance between two grid points (important for ghost moves.)
        return math.sqrt((loc_1[0]-loc_2[0])**2 + (loc_1[1]-loc_2[1])**2)

    def closest_move_to_target(self):
        move = self.valid_moves[0]
        for dir in self.valid_moves:
            if ghost.distance([self.grid_location[0]+dir[0], self.grid_location[1]+dir[1]], self.target) \
            < ghost.distance([self.grid_location[0] + move[0], self.grid_location[1]+move[1]], self.target):
                move = dir
        self.current_dir = move

    def random_move(self):
        rand_num = random.randint(0, len(self.valid_moves)-1)
        self.current_dir = self.valid_moves[rand_num]

    def update_valid_moves(self):
        super(ghost, self).update_valid_moves()

        if [0-self.current_dir[0], 0-self.current_dir[1]] in self.valid_moves:
            self.valid_moves.remove([0-self.current_dir[0], 0-self.current_dir[1]])
        #(ensures that the ghost cannot turn back on itself.)
        #THERE ARE ALSO SOME CELLS THE GHOST MAY NOT MOVE UP FROM. WE WORRY
        #ABOUT THESE LATER!

    def ghost_move(self,Pacman,dt,other_ghost = None):
        if self.movement_mode not in ["moving_in", "stay_in_house", "moving_out"]:
            self.get_target(Pacman, other_ghost)
            self.update_valid_moves()
            if self.current_dir in self.valid_moves and len(self.valid_moves) == 1:
                self.move(self.current_dir)
            else:
                self.fractional_coordinates()
                if (self.current_dir == [1,0] and self.frac_y < 0.5 - self.speed/(2*self.board.grid_square_height)) or \
                (self.current_dir == [-1,0] and self.frac_y > 0.5 + self.speed/(2*self.board.grid_square_height)) or \
                (self.current_dir == [0,1] and self.frac_x < 0.5 - self.speed/(2*self.board.grid_square_width)) or \
                (self.current_dir == [0,-1] and self.frac_x > 0.5 + self.speed/(2*self.board.grid_square_width)):
                    pass #force the ghost to go deeper into the corner than PacMan,
                    #giving pacamn a turning advantage over his rivals!
                elif not((self.current_dir == [1,0] and self.frac_y > 0.5 + self.speed/(2*self.board.grid_square_height)) or \
                (self.current_dir == [-1,0] and self.frac_y < 0.5 - self.speed/(2*self.board.grid_square_height)) or \
                (self.current_dir == [0,1] and self.frac_x > 0.5 + self.speed/(2*self.board.grid_square_width)) or \
                (self.current_dir == [0,-1] and self.frac_x < 0.5 - self.speed/(2*self.board.grid_square_width))):
                    if self.movement_mode == "frightened":
                        self.random_move()
                    else:
                        self.closest_move_to_target()
                self.move(self.current_dir)

        elif self.movement_mode == "moving_in":
            if self.y>self.board.grid_square_height*18.5:
                self.y -= self.speed
                self.x = self.board.grid_square_width*14
            else:
                if self.ghost_type =="clyde" and self.x<self.board.grid_square_width*16:
                    self.x += self.speed
                elif self.ghost_type == "inky" and self.x>self.board.grid_square_width*12:
                    self.x -= self.speed
                else:
                    self.init_movement_mode("stay_in_house")
        elif self.movement_mode == "stay_in_house":
            self.stay_in_house()
        elif self.movement_mode == "moving_out":
            if not(14*self.board.grid_square_width - 2*self.speed<self.x< \
            14*self.board.grid_square_width + 2*self.speed):
                if self.x<14*self.board.grid_square_width - 2*self.speed:
                    self.x += self.speed
                else:
                    self.x -= self.speed
            elif self.y < self.board.grid_square_height*21.5:
                self.y += self.speed
            else:
                if self.frightened == True:
                    self.init_movement_mode("frightened")
                else:
                    self.init_movement_mode(self.wave_mode)

        if self.movement_mode == "dead":
            if self.current_dir == [0,-1]:
                self.image = resources.dead_eyes[0]
            elif self.current_dir == [0,1]:
                self.image = resources.dead_eyes[1]
            elif self.current_dir == [1,0]:
                self.image = resources.dead_eyes[2]
            elif self.current_dir == [-1,0]:
                self.image = resources.dead_eyes[3]
            if self.grid_location == self.target:
                self.init_movement_mode("moving_in")
        elif self.frightened == True:
            if self.ghost_state<240:
                self.image = resources.frightened_states[0][(math.floor(self.ghost_state/10))%2]
            else:
                self.image = resources.frightened_states[(math.floor(self.ghost_state/20))%2][(math.floor(self.ghost_state/10))%2]
            self.ghost_state = (self.ghost_state+1)%480 # This timer will in general be a func of level num
            if self.ghost_state ==0:
                self.frightened = False
                self.speed_multiplier = 1
                if self.movement_mode not in ["moving_in", "stay_in_house", "moving_out"]:
                    self.init_movement_mode(self.wave_mode)
        else:
            self.ghost_state= (self.ghost_state+1)%20
            if self.current_dir == [0,-1]:
                self.image = self.ghost_states[0][math.floor(self.ghost_state/10)]
            elif self.current_dir == [0,1]:
                self.image = self.ghost_states[1][math.floor(self.ghost_state/10)]
            elif self.current_dir == [1,0]:
                self.image = self.ghost_states[2][math.floor(self.ghost_state/10)]
            elif self.current_dir == [-1,0]:
                self.image = self.ghost_states[3][math.floor(self.ghost_state/10)]
