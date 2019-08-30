import pyglet
from pyglet.window import key
import math
from game import resources, pacsprite, board, PacMan, ghost, physical_object, level_controllers, score_object, scoring

sprite_board = board.board(size = (36*8*2, 28*8*2))
pellet_board = board.board(size = (36*8*2, 28*8*2), grid_type = "pellet_grid")
height, width = sprite_board.size[0], sprite_board.size[1]
main_batch = pyglet.graphics.Batch()

game_window = pyglet.window.Window(width,height)
board_img = resources.board_img
board_img.width, board_img.height = width, height
resources.center_image(board_img)

title_img = resources.title_img
title_img.width, title_img.height = width, height
resources.center_image(title_img)

game_scale = math.sqrt(sprite_board.grid_square_width*sprite_board.grid_square_height/64)

game_state = "title_screen"
free_index = 0 #used for timing respawns as well as ghost eating points
score = 0
(low_score, high_score) = scoring.get_low_and_high_scores()
score_text, high_score_text = "0", "0"

Pacman = PacMan.Pacman(spawn_location = (width/2, height/4+sprite_board.grid_square_height/2),
    batch = main_batch, board = sprite_board)
Pacman.scale = game_scale
Pacman.universal_speed = 0.9*game_scale
for life in Pacman.lives:
    life.scale = 0.9*game_scale

Blinky = ghost.ghost(spawn_location = [width/2, 11/18*height - sprite_board.grid_square_height/2],
    img = resources.blinky_states[0][0],
    ghost_type = "blinky",
    batch = main_batch,
    board = sprite_board)
Blinky.scale = game_scale
Blinky.universal_speed = 0.9*game_scale

Pinky = ghost.ghost(spawn_location = [width/2, height/2+1.5*sprite_board.grid_square_height],
    img = resources.pinky_states[0][0],
    ghost_type = "pinky",
    batch = main_batch,
    board = sprite_board)
Pinky.scale = game_scale
Pinky.universal_speed = 0.9*game_scale

Clyde = ghost.ghost(spawn_location = [width/2 + 2*sprite_board.grid_square_width, height/2-0.5*sprite_board.grid_square_height],
    img = resources.clyde_states[0][0],
    ghost_type = "clyde",
    batch = main_batch,
    board = sprite_board)
Clyde.scale = game_scale
Clyde.universal_speed = 0.9*game_scale

Inky = ghost.ghost(spawn_location = [width/2 - 2*sprite_board.grid_square_width, height/2-0.5*sprite_board.grid_square_height],
    img = resources.inky_states[0][0],
    ghost_type = "inky",
    batch = main_batch,
    board = sprite_board)
Inky.scale = game_scale
Inky.universal_speed = 0.9*game_scale

Ghosts = [Blinky, Pinky, Inky, Clyde] #Note that the last three are the "preferred" ghost order for spawning.
preferred_ghost_index = 1

def create_pellets(energiser_pellet_locations = [[9,1], [9,26], [29,1], [29,26]], game_scale = 1):
    pellet_dictionary = {}
    for i in range(pellet_board.grid.shape[0]):
        for j in range(pellet_board.grid.shape[1]):
            if pellet_board.grid[i,j] == 1:
                if [i,j] not in energiser_pellet_locations:
                    pellet_dictionary[str(i) + "," + str(j)] = physical_object.physical_object(img = resources.pellet_img,
                        y = pellet_board.grid_square_height*(i+1/2),
                        x = pellet_board.grid_square_width*(j+1/2),
                        batch = main_batch, board = pellet_board)
                    pellet_dictionary[str(i) + "," + str(j)].scale = game_scale
                else:
                    pellet_dictionary[str(i) + "," + str(j)] = physical_object.physical_object(img = resources.energiser_pellet_img,
                        y = pellet_board.grid_square_height*(i+1/2) ,
                        x = pellet_board.grid_square_width*(j+1/2),
                        batch = main_batch, board = pellet_board)
                    pellet_dictionary[str(i) + "," + str(j)].scale = game_scale
    return pellet_dictionary

energiser_pellet_locations = [[9,1], [9,26], [29,1], [29,26]]
pellet_dictionary = create_pellets(game_scale = game_scale)

menu_controls = key.KeyStateHandler()
game_window.push_handlers(Pacman.key_handler)
game_window.push_handlers(menu_controls)

@game_window.event
def on_draw():
    global score_text, high_score_text, score, high_score, name_text
    high_score = max(high_score, score)
    if game_state == "title_screen":
        title_img.blit(width/2,height/2)
        high_score_text = level_controllers.score_board_imgs(high_score)
        for i in range(len(high_score_text)):
            high_score_text[i].height = sprite_board.grid_square_height
            high_score_text[i].width = sprite_board.grid_square_width
            high_score_text[i].blit((i+15)*sprite_board.grid_square_width,
                0.8*height)
    elif game_state == "game_over":
        game_window.clear()
        board_img.blit(width/2,height/2)
        resources.game_over_img.height = sprite_board.grid_square_height
        resources.game_over_img.width = sprite_board.grid_square_width*10
        resources.center_image(resources.game_over_img)
        resources.game_over_img.blit(width/2,height*15.5/36)
    else:
        game_window.clear()
        board_img.blit(width/2,height/2)
        main_batch.draw()
        if game_state == "level_start":
            resources.ready_img.blit(width/2,height*15.5/36)

        score_text = level_controllers.score_board_imgs(score)
        for i in range(len(score_text)):
            score_text[i].height = sprite_board.grid_square_height
            score_text[i].width = sprite_board.grid_square_width
            score_text[i].blit((i+1)*sprite_board.grid_square_width,
                height - 1.5*sprite_board.grid_square_height)

        high_score_text = level_controllers.score_board_imgs(high_score)
        for i in range(len(high_score_text)):
            high_score_text[i].height = sprite_board.grid_square_height
            high_score_text[i].width = sprite_board.grid_square_width
            high_score_text[i].blit((i+15)*sprite_board.grid_square_width,
                height - 1.5*sprite_board.grid_square_height)

level = 0
level_timer = 0
energiser_points = [200, 400, 800, 1600]
score_objects = []

def update(dt):
    global game_state, free_index, Ghosts, preferred_ghost_index,\
        energiser_pellet_locations, pellet_dictionary, level, level_timer,\
        score, score_objects, game_scale
    if game_state == "title_screen":
        if menu_controls[key.SPACE]:
            game_state = "level_start"
    elif game_state == "level_start":
        if free_index == 0:
            pellet_dictionary = create_pellets(game_scale = game_scale)
            total_dots_eaten = 0
            score_objects = []
            preferred_ghost_index = 1
            level_timer = 0
            level += 1
            Pacman.respawn()
            for Ghost in Ghosts:
                Ghost.respawn()
                Ghost.frightened = False
                Ghost.init_movement_mode("stay_in_house")
                Ghost.wave_mode = "scatter"
            Pacman.died_this_level = False
        elif free_index == 120:
            game_state = "playing"
        free_index += 1
    elif game_state == "playing":
        Pacman.update(dt)
        try:
            if Pacman.grid_location not in energiser_pellet_locations:
                pellet_dictionary[str(Pacman.grid_location[0]) + "," + str(Pacman.grid_location[1])].delete()
                del pellet_dictionary[str(Pacman.grid_location[0]) + "," + str(Pacman.grid_location[1])]
                score += 10
                if Pacman.pac_waka == 0:
                    resources.waka1_sound.play()
                else:
                    resources.waka2_sound.play()
                Pacman.pac_waka = (Pacman.pac_waka + 1)%2
                if Pacman.died_this_level:
                    for Ghost in Ghosts:
                        Ghost.dot_counter +=1
                else:
                    if Ghosts[preferred_ghost_index].dot_counter == Ghosts[preferred_ghost_index].dot_limit:
                        if preferred_ghost_index != len(Ghosts)-1:
                            preferred_ghost_index += 1
                    Ghosts[preferred_ghost_index].dot_counter += 1
            else:
                pellet_dictionary[str(Pacman.grid_location[0]) + "," + str(Pacman.grid_location[1])].delete()
                del pellet_dictionary[str(Pacman.grid_location[0]) + "," + str(Pacman.grid_location[1])]
                score+=50
                Pacman.energise()
                free_index = 0
                for Ghost in Ghosts:
                    if Ghost.movement_mode in ["chase", "scatter", "frightened"]:
                        Ghost.init_movement_mode("frightened")
                    elif Ghost.movement_mode != "dead":
                        Ghost.frightened = True
        except KeyError:
            pass
        if len(pellet_dictionary) != 0:
            level_timer += 1
            de_energise = 0
            game_states = []
            for Ghost in Ghosts:
                level_controllers.wave_controller(level, level_timer, Ghost)
                if Ghost.ghost_type == "inky":
                    Ghost.ghost_move(Pacman, dt, Blinky)
                else:
                    Ghost.ghost_move(Pacman,dt)
                if Pacman.energised and Ghost.movement_mode!="frightened":
                    de_energise +=1
                game_states.append(Pacman.collides_with_ghost(Ghost))
            for state in game_states:
                if state == "game_over":
                    game_state = "game_over"
                    break
                elif state == "respawning":
                    game_state = "respawning"
                    free_index = 0
                    for Ghost in Ghosts:
                        Ghost.respawn()
                        Ghost.frightened = False
                        Ghost.init_movement_mode("stay_in_house")
                        if Ghost.ghost_type == "blinky":
                            Ghost.dot_limit = 0
                        elif Ghost.ghost_type == "pinky":
                            Ghost.dot_limit = 7
                        elif Ghost.ghost_type == "inky":
                            Ghost.dot_limit = 16
                        elif Ghost.ghost_type == "clyde":
                            Ghost.dot_limit = 32
                    break
                elif state == "score":
                    score += 200*(2**free_index)
                    score_objects.append(score_object.score_object(
                        img = resources.scores[free_index], board = sprite_board,
                        x = Pacman.x, y = Pacman.y, time = 0.5, batch=main_batch))
                    score_objects[len(score_objects)-1].scale = game_scale
                    free_index += 1
            if de_energise==len(Ghosts):
                Pacman.de_energise(dt)
        else:
            game_state = "level_start"
            free_index = 0
    elif game_state == "respawning":
        if free_index == 60:
            game_state = "playing"
        else:
            free_index += 1

pyglet.clock.schedule_interval(update, 1/120.0)

pyglet.app.run()
