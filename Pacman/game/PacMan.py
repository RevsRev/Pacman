import pyglet
import math
from pyglet.window import key
from game import pacsprite, resources, physical_object

class Pacman(pacsprite.pacsprite):

    def __init__(self, lives =3, *args, **kwargs):
        super(Pacman, self).__init__(img = resources.pac1_img, *args, **kwargs)
        self.key_handler = key.KeyStateHandler()
        self.pacstates = {0: resources.pac1_img, 1: resources.pac2_img}
        self.pacstate = 0 #controls which sprite image is shown.
        self.pac_waka = 0 #controls the wakawaka sounds:D
        self.energised = False
        self.lives = []
        self.died_this_level = False #If Pacman has died, ghost respawn logic will change.
        for i in range(lives):
            self.add_life()

    def add_life(self):
        self.lives.append(physical_object.physical_object(board = self.board,
            img = resources.pac1_img, batch = self.batch,
            x = (2.5+2*len(self.lives))*self.board.grid_square_width,
            y = self.board.grid_square_height))

    def energise(self):
        self.energised=True
        self.counter = 0
        pyglet.clock.schedule_once(self.de_energise, self.count_limit/120)

    def de_energise(self, dt):
        self.energised=False

    def collides_with_ghost(self,Ghost):
        if self.collides_with(Ghost):
            if Ghost.movement_mode in ["chase", "scatter"]:
                self.respawn()
                self.died_this_level = True
                Ghost.respawn()
                Ghost.init_movement_mode("stay_in_house")
                if len(self.lives)>0:
                    self.lives[len(self.lives)-1].delete()
                    del self.lives[len(self.lives)-1]
                    return "respawning"
                else:
                    return "game_over"
            elif Ghost.movement_mode == "frightened":
                Ghost.init_movement_mode("dead")
                Ghost.dot_limit = 0
                resources.ghost_eat_sound.play()
                return "score"
            else:
                return "dead_collision" #not necessary, but included for completeness.
        else:
            return "no_collision"

    def update(self, dt):
        if self.key_handler[key.LEFT]:
            if [0,-1] in self.valid_moves:
                self.current_dir = [0,-1]
        if self.key_handler[key.UP]:
            if [1,0] in self.valid_moves:
                self.current_dir = [1,0]
        if self.key_handler[key.RIGHT]:
            if [0,1] in self.valid_moves:
                self.current_dir = [0,1]
        if self.key_handler[key.DOWN]:
            if [-1,0] in self.valid_moves:
                self.current_dir = [-1,0]
        self.move(self.current_dir)

        if self.current_dir == [0,1]:
            self.rotation = 0
        if self.current_dir == [0,-1]:
            self.rotation = 180
        if self.current_dir == [1,0]:
            self.rotation = 270
        if self.current_dir == [-1,0]:
            self.rotation = 90

        if self.current_dir in self.valid_moves:
            self.image = self.pacstates[math.floor(self.pacstate/4)]
            self.pacstate = (self.pacstate + 1)%8

        if self.energised:
            if self.counter%16 ==0:
                resources.energised_loop.play()
            self.counter += 1
