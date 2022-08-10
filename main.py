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
from data.scripts.particle_generator import *
from data.scripts.glow import *
from data.scripts.debug import *
 
# Initialize ----------------------------------------------------------------- #
pygame.display.set_caption('Obama Hacking 101')
clock = pygame.time.Clock()

button = Button(pygame.Rect(20, 130, 100, 28), 'Play', 'basic')

player = Entity([100, 100], 'dark_player', offset=[9, 0], max_vel=2)

text = '''the quick brown fox jumps over the lazy dog?
THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG!'''
text = ''
g = Glow([(255, 200, 100), (255, 100, 0), (255, 0, 0)], [3, 6, 9], [255, 255, 255])
img = pygame.image.load('data/img/particles/circle.png')
#                    ParticleGenerator(rate, rate_randomness, random_change, vel_randomness, pos, vel, friction, initial_img, alpha, changed_alpha, changed_size, glow)
# particle_generator = ParticleGenerator(7, 0, 0, [0.3, 1], [1, 1], [0, -2], 0, img, 255, 2, 0.01, g)
particle_generator = ParticleGenerator(1, 0, 0, [0.3, 1], [1, 1], [0, -2], 0, None, 50, 1, 0.01, g)

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
    canvas.fill((100, 100, 100))
    canvas.fill((50, 50, 50))
    
    render_wrapped_text(canvas, (mx + 10, my), text, font_database['basic'], (20, 20, 20))
    
    if right_down:
        player.vel[0] += 0.1
        player.set_flip([False, False])
        player.set_action('walk')
    if left_down:
        player.vel[0] -= 0.1
        player.set_flip([True, False])
        player.set_action('walk')
    if not(right_down) and not(left_down):
        player.set_action('idle')
    player.update()
    
    particle_generator.pos = [mx, my]
    particle_generator.update_and_render(canvas, [0, 0.05])
        
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
{len(particle_generator.particles) = }
'''
    render_variables(screen, debug_text)    

    # Update ----------------------------------------------------------------- #
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
