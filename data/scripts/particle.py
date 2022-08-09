import pygame
from pygame.locals import *
from random import uniform
from .config import colorkey
from .core_functions import center_blit, get_angle
from .movable_object import *
from math import atan, pi

class Particle(MovableObject):
    """
    visual attributes -- attributes which determine the initial appearance of 
    the Particle:
    - alpha (defined with argument)
    - size (not defined with argument)
    - glow.radius (defined with argument)
    
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
    
    def __init__(self, random_change, vel_randomness, pos, vel, friction, initial_img, alpha, changed_alpha, 
                 changed_size, glow, angle_at_vel=False, max_vel=None, size=1, center=True):
        self.random_change = random_change
        self.vel_randomness = vel_randomness
        vel[0] = self.apply_random_change(vel[0], vel_randomness[0], 1)
        vel[1] = self.apply_random_change(vel[1], vel_randomness[1], 1)
        
        if center:
            if initial_img:
                pos[0] -= initial_img.get_width() / 2
                pos[1] -= initial_img.get_height() / 2
        super().__init__(pos, vel, friction, max_vel)
        self.initial_img = initial_img
        if initial_img:
            self.initial_img = initial_img.convert()
            self.initial_img.set_colorkey(colorkey)
        self.size = self.apply_random_change(size, changed_size, random_change)
        self.changed_size = changed_size
        self.alpha = self.apply_random_change(alpha, changed_alpha, random_change)
        self.changed_alpha = changed_alpha
        self.glow = glow
        self.angle_at_vel = angle_at_vel
        
    @property
    def img(self):
        if self.initial_img:
            img = self.initial_img.copy()
            img.set_alpha(self.alpha)
            if self.angle_at_vel:
                try:
                    angle = get_angle(self.vel)
                    img = pygame.transform.rotate(img, -angle)
                except ZeroDivisionError:
                    pass
                angle = 90
                print(angle, self.vel)
            img = pygame.transform.scale(img, (img.get_width() * self.size, img.get_height() * self.size))
            return img
        
    def render_glow(self, surface):
        # NOTE: The value of self.glow.alphas does not matter because the 
        # Particle's glow is dependant on self.glow
        
        for surf in self.glow.surfs:
            surf.set_alpha(self.alpha)
            surf = pygame.transform.scale(surf, (surf.get_width() * self.size, surf.get_height() * self.size))
            
            if self.img:
                pos = (
                    self.pos[0] + self.img.get_width() / 2 - surf.get_width() / 2,
                    self.pos[1] + self.img.get_height() / 2 - surf.get_height() / 2
                )
            else:
                pos = (self.pos[0] - surf.get_width() / 2, 
                       self.pos[1] - surf.get_height() / 2)
            
            # Because of a bug in pygame, I can't render surf directly to the 
            # display, I must instead create a copy of it and render that 
            # instead.
            tmp_surface = pygame.Surface(surf.get_size())
            tmp_surface.blit(surf, (0, 0))
            surface.blit(tmp_surface, pos, special_flags=BLEND_RGB_ADD)            
            
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
        if self.glow:
            self.render_glow(surface)
        if self.initial_img:
            surface.blit(self.img, self.pos)
            
    @staticmethod
    def apply_random_change(target_attribute, changed_attribute, randomness):
        min_value = target_attribute - changed_attribute * randomness
        max_value = target_attribute + changed_attribute * randomness
        return uniform(min_value, max_value)