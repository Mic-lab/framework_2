import pygame
from .config import SCREEN_SIZE, CANVAS_SIZE

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
canvas = pygame.Surface(CANVAS_SIZE)