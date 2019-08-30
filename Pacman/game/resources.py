import pyglet

pyglet.resource.path = ['C:/Users/Eddie Revell/Documents/Learning Python/Games/Pacman/resources']
pyglet.resource.reindex()

#IMAGES

def center_image(image):
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

board_img = pyglet.resource.image("board.png")
title_img = pyglet.resource.image("title_screen.png")
center_image(title_img)

pac0_img = pyglet.resource.image("pacman_sprites/pac0.png")
center_image(pac0_img)
pac1_img = pyglet.resource.image("pacman_sprites/pac1.png")
center_image(pac1_img)
pac2_img = pyglet.resource.image("pacman_sprites/pac2.png")
center_image(pac2_img)

blinky_states = [[pyglet.resource.image("blinky_sprites/blinky_left0.png"),
    pyglet.resource.image("blinky_sprites/blinky_left1.png")],
    [pyglet.resource.image("blinky_sprites/blinky_right0.png"),
    pyglet.resource.image("blinky_sprites/blinky_right1.png")],
    [pyglet.resource.image("blinky_sprites/blinky_up0.png"),
    pyglet.resource.image("blinky_sprites/blinky_up1.png")],
    [pyglet.resource.image("blinky_sprites/blinky_down0.png"),
    pyglet.resource.image("blinky_sprites/blinky_down1.png")]]
for directions in blinky_states:
    for blinky in directions:
        center_image(blinky)

pinky_states = [[pyglet.resource.image("pinky_sprites/pinky_left0.png"),
    pyglet.resource.image("pinky_sprites/pinky_left1.png")],
    [pyglet.resource.image("pinky_sprites/pinky_right0.png"),
    pyglet.resource.image("pinky_sprites/pinky_right1.png")],
    [pyglet.resource.image("pinky_sprites/pinky_up0.png"),
    pyglet.resource.image("pinky_sprites/pinky_up1.png")],
    [pyglet.resource.image("pinky_sprites/pinky_down0.png"),
    pyglet.resource.image("pinky_sprites/pinky_down1.png")]]
for directions in pinky_states:
    for pinky in directions:
        center_image(pinky)

clyde_states = [[pyglet.resource.image("clyde_sprites/clyde_left0.png"),
    pyglet.resource.image("clyde_sprites/clyde_left1.png")],
    [pyglet.resource.image("clyde_sprites/clyde_right0.png"),
    pyglet.resource.image("clyde_sprites/clyde_right1.png")],
    [pyglet.resource.image("clyde_sprites/clyde_up0.png"),
    pyglet.resource.image("clyde_sprites/clyde_up1.png")],
    [pyglet.resource.image("clyde_sprites/clyde_down0.png"),
    pyglet.resource.image("clyde_sprites/clyde_down1.png")]]
for directions in clyde_states:
    for clyde in directions:
        center_image(clyde)

inky_states = [[pyglet.resource.image("inky_sprites/inky_left0.png"),
    pyglet.resource.image("inky_sprites/inky_left1.png")],
    [pyglet.resource.image("inky_sprites/inky_right0.png"),
    pyglet.resource.image("inky_sprites/inky_right1.png")],
    [pyglet.resource.image("inky_sprites/inky_up0.png"),
    pyglet.resource.image("inky_sprites/inky_up1.png")],
    [pyglet.resource.image("inky_sprites/inky_down0.png"),
    pyglet.resource.image("inky_sprites/inky_down1.png")]]
for directions in inky_states:
    for inky in directions:
        center_image(inky)

frightened_states = [[pyglet.resource.image("frightened_ghosts/blue0.png"),
    pyglet.resource.image("frightened_ghosts/blue1.png")],
    [pyglet.resource.image("frightened_ghosts/white0.png"),
    pyglet.resource.image("frightened_ghosts/white1.png")]]
for colors in frightened_states:
    for index in colors:
        center_image(index)

dead_eyes = [pyglet.resource.image("dead_ghosts/eyes_left.png"),
    pyglet.resource.image("dead_ghosts/eyes_right.png"),
    pyglet.resource.image("dead_ghosts/eyes_up.png"),
    pyglet.resource.image("dead_ghosts/eyes_down.png")]
for eyes in dead_eyes:
    center_image(eyes)

pellet_img = pyglet.resource.image("pellet.png")
center_image(pellet_img)
energiser_pellet_img = pyglet.resource.image("energiser_pellet.png")
center_image(energiser_pellet_img)

ready_img = pyglet.resource.image("fonts/ready.png")
center_image(ready_img)
game_over_img = pyglet.resource.image("fonts/game_over.png")
center_image(game_over_img)
high_score_img = pyglet.resource.image("fonts/high_score_sign.png")
center_image(high_score_img)

numbers = []
for i in range(10):
    numbers.append(pyglet.resource.image("fonts/numbers/num_" + str(i) + ".png"))
    center_image(numbers[i])

scores = []
for i in range(4):
    scores.append(pyglet.resource.image("fonts/score_" + str(200*(2**i)) + ".png"))
    center_image(scores[i])


#SOUNDS

waka1_sound = pyglet.resource.media("Pacman_Waka1.wav", streaming = False)
waka2_sound = pyglet.resource.media("Pacman_Waka2.wav", streaming = False)
energised_loop = pyglet.resource.media("Pacman_energised2.wav", streaming = False)
ghost_eat_sound = pyglet.resource.media("Pacman_Ghost_Eat.wav", streaming = False)
