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
from data.scripts.animated_particle import *
from data.scripts.animated_particle_generator import *
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
particle_generator = ParticleGenerator(20, 0, 0, [0.3, 1], [1, 1], [0, -2], 0, img, 50, 1, 0.01, None)

img = pygame.image.load('data/img/particles/andre.png')
particle_generator = ParticleGenerator(20, 0, 0, [0.3, 1], [1, 1], [0, -2], 0, None, 50, 1, 0.01, g)

animated_particle_generator = AnimatedParticleGenerator(1, 0, [1, 0], [50, 50], [0, 0], 0, 'circle', (200, 200, 255), randomize_particle_duration=False)

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
    animated_particle_generator.pos = [player.pos[0], player.pos[1] + 8]
    animated_particle_generator.update_and_render(canvas)
        
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
##    print(particle_animation_database)

pygame.quit()
sys.exit()
