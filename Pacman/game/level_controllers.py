from game import ghost, resources
from pyglet.window import key

def wave_controller(level_num, level_timer,Ghost):
    if level_num == 1:
        if level_timer == 7*120:
            Ghost.switch_wave_mode()
        elif level_timer == 27*120:
            Ghost.switch_wave_mode()
        elif level_timer == 34*120:
            Ghost.switch_wave_mode()
        elif level_timer == 54*120:
            Ghost.switch_wave_mode()
        elif level_timer == 59*120:
            Ghost.switch_wave_mode()
        elif level_timer == 79*120:
            Ghost.switch_wave_mode()
        elif level_timer == 84*120:
            Ghost.switch_wave_mode()
    elif level_num == 2:
        if level_timer == 7*120:
            Ghost.switch_wave_mode()
        elif level_timer == 27*120:
            Ghost.switch_wave_mode()
        elif level_timer == 34*120:
            Ghost.switch_wave_mode()
        elif level_timer == 54*120:
            Ghost.switch_wave_mode()
        elif level_timer == 59*120:
            Ghost.switch_wave_mode()
    elif level_num>=5:
        if level_timer == 5*120:
            Ghost.switch_wave_mode()
        elif level_timer == 25*120:
            Ghost.switch_wave_mode()
        elif level_timer == 30*120:
            Ghost.switch_wave_mode()
        elif level_timer == 50*120:
            Ghost.switch_wave_mode()
        elif level_timer == 55*120:
            Ghost.switch_wave_mode()

def score_board_imgs(score):
    """Take in integer score and format the image (font) for outputing the score in_game
    Score is limited to 100,000,000 (hopefully should be an issue!)"""
    score_str = str(score)
    score_text = []
    for i in range(len(score_str)):
        score_text.append(resources.numbers[int(score_str[i])])
    return score_text
