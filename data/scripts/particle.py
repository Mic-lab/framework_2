import pygame
from random import uniform
from .config import colorkey
from .movable_object import *

class Particle(MovableObject):
    """
    visual attributes -- attributes which determine the initial appearance of 
    the Particle:
    - alpha (defined with argument)
    - size (not defined with argument)
    TODO: Add more
    
    There is a changed attribute which corresponds to each visual attribute
    (ex: alpha and changed_alpha). The changed attribute represents how much the
    visual attribute changes per frame. The changes are executed in the
    update_appearance method. Note that random_change is not quite a change
    attribute.
    
    Randomized factors for a particle:
    - changed attributes
    - vel
    
    random_change randomly varies how much the changed attributes impact the 
    visual attributes. I figured that having a randomness for each individual
    change attribute would make it time consuming to use the class. So instead
    this one attribute handles all the random changes. 
    
    random_vel ramdomly varies the initial vel
    """
    
    def __init__(self, random_change, vel_randomness, pos, vel, friction, initial_img, alpha, changed_alpha, changed_size, max_vel=None, size=1):
        self.random_change = random_change
        self.vel_randomness = vel_randomness
        vel[0] = self.apply_random_change(vel[0], vel_randomness[0], 1)
        vel[1] = self.apply_random_change(vel[1], vel_randomness[1], 1)
        super().__init__(pos, vel, friction, max_vel)
        self.initial_img = initial_img.convert()
        self.initial_img.set_colorkey(colorkey)
        self.size = self.apply_random_change(size, changed_size, random_change)
        self.changed_size = changed_size
        self.alpha = self.apply_random_change(alpha, changed_alpha, random_change)
        self.changed_alpha = changed_alpha
        
    @property
    def img(self):
        img = self.initial_img.copy()
        img.set_alpha(self.alpha)
        img = pygame.transform.scale(img, (img.get_width() * self.size, img.get_height() * self.size))
        return img
        
    def update(self, vel_change=None):
        if vel_change:
            self.vel[0] += vel_change[0]
            self.vel[1] += vel_change[1]
        super().update()
        self.update_appearance()
        return self.size <= 0 or self.alpha <= 0
        
    def update_appearance(self):
        self.alpha -= self.changed_alpha
        self.size -= self.changed_size
        
    def render(self, surface):
        surface.blit(self.img, self.pos)
                
    @staticmethod
    def apply_random_change(initial_attribute, changed_attribute, randomness):
        min_value = initial_attribute - changed_attribute * randomness
        max_value = initial_attribute + changed_attribute * randomness
        return uniform(min_value, max_value)