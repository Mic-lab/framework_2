import pygame
from .core_functions import *

pygame.init()
font = pygame.font.SysFont('consolas', 16)

def render_variables(surf, text):
    text = text.split('\n')
    y = 0
    for line in text:
        img = font.render(line, True, (20, 20, 20))
        surf.blit(img, (0, y))
        y += img.get_height()
    