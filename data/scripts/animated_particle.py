import pygame
from animations import *
from .config import particle_path

class AnimatedParticled(MovableObject):
    
    def __init__(self, pos, vel, friction, imgs, type_, max_vel=None):
        super().__init__(pos, vel, friction, max_vel)
        self.type = type_
        # load_animation(f'{particle_path}/{type_}')
        self.animation_frame = 0
        self.game_frame = 0
        
    def update(self, vel_change=None):
        self.game_frame