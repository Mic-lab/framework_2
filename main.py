import pygame
import time
import sys
import random
from pygame.locals import *
from data.scripts.screen import *
from data.scripts.core_functions import *
from data.scripts.entity import *
from data.scripts.font_functions import *
from data.scripts.button import *
from data.scripts.debug import *

# Initialize ----------------------------------------------------------------- #
pygame.display.set_caption('Obama Hacking 101')
clock = pygame.time.Clock()

button = Button(pygame.Rect(20, 130, 100, 28), 'Play', 'basic')

player = Entity([100, 100], 'dark_player', offset=[9, 0], max_vel=2)

text = '''the quick brown fox jumps over the lazy dog?
THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG!'''
text = ''

mouse_down = False
right_down = False
left_down = False

# Game loop ------------------------------------------------------------------ #
run = True
while run:

    # Event loop ------------------------------------------------------------- #
    clicked = False
    
    for event in pygame.event.get():
        
        if event.type == QUIT:
            run = False
            
        if event.type == MOUSEBUTTONDOWN:
            mouse_down = True
            clicked = True
            
        if event.type == MOUSEBUTTONUP:
            mouse_down = False
            
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                right_down = True
            if event.key == K_LEFT:
                left_down = True
                
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                right_down = False
            if event.key == K_LEFT:
                left_down = False
                
            
    mx, my = pygame.mouse.get_pos()
    mx /= SCALE
    my /= SCALE

    # Render ----------------------------------------------------------------- #
    canvas.fill((190, 200, 200))
    if right_down:
        player.vel[0] += 0.1
        player.set_flip([False, False])
        player.action = 'walk'
    if left_down:
        player.vel[0] -= 0.1
        player.set_flip([True, False])
        player.action = 'walk'
    if not(right_down) and not(left_down):
        player.action = 'idle'
    player.update()
    render_wrapped_text(canvas, (mx + 10, my), text, font_database['basic'], (20, 20, 20))
    # center_blit([canvas, player.frame_data['img']])
    player.render(canvas)
    button.update(mx, my, mouse_down, clicked)
    button.render(canvas)
    
    screen.blit(pygame.transform.scale(canvas, SCREEN_SIZE), (0, 0))
    debug_text = f'''FPS = {round(clock.get_fps(), 1)}
{SCREEN_SIZE = }
{CANVAS_SIZE = }
{player.vel = }
{player.pos = }
{player.flip = }
'''
    render_variables(screen, debug_text)    

    # Update ----------------------------------------------------------------- #
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
