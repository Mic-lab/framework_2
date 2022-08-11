import pygame
from .animations import *
from .movable_object import MovableObject
from .config import particle_path
from .animation_manager import AnimationManager

class AnimatedParticle(MovableObject):
    
    def __init__(self, pos, vel, friction, type_, rgb, randomize_duration, max_vel=None):
        super().__init__(pos, vel, friction, max_vel)
        load_particle_animation(f'{particle_path}/{type_}', rgb)
        self.animation_manager = AnimationManager(particle_animation_database[f'{type_} {rgb}'], randomize_duration=randomize_duration)
        
    def update(self, vel_change=None):
        super().update()
        return self.animation_manager.update()
        
    def render(self, surf):
        surf.blit(self.animation_manager.img, self.pos)