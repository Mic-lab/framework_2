import pygame
from .particle import *
from .movable_object import *

class ParticleGenerator(MovableObject):
    
    def __init__(self, rate, rate_randomness, random_change, vel_randomness, pos, vel, friction, initial_img, alpha, changed_alpha, changed_size, max_vel=None, size=1, duration=None):
        self.rate = rate
        self.rate_randomness = rate_randomness
        self.duration = None
        self.particles = []
        self.frame_count = 0
            
        # Particle attributes
        self.random_change = random_change
        self.vel_randomness = vel_randomness
        super().__init__(pos, vel, friction, max_vel)
        self.initial_img = initial_img.convert()
        self.initial_img.set_colorkey(colorkey)
        self.size = size
        self.changed_size = changed_size
        self.alpha = alpha
        self.changed_alpha = changed_alpha
        
    def get_particle(self):
        return Particle(self.random_change, self.vel_randomness.copy(), self.pos.copy(), self.vel.copy(), self.friction, self.initial_img, self.alpha, self.changed_alpha, self.changed_size, max_vel=self.max_vel, size=self.size)
        
    def update_and_render(self, surface, vel_change=None):
        """This function updates and renders, instead of doing both of those
        methods seperatly. This is preferable then calling both methods together
        because I don't need to iterate through particles twice, which will be less effecient
        when it comes to performance.
        """
        if vel_change:
            vel_change = vel_change.copy()
            
        self.frame_count += 1
        
        while self.frame_count >= 1/self.rate:
            self.frame_count -= 1/self.rate
            self.particles.append(self.get_particle())
                
                
        i = 0
        while i < len(self.particles):
            particle = self.particles[i]
            invisible = particle.update(vel_change)
            if invisible:
                self.particles.pop(i)
            else:
                particle.render(surface)
                i += 1
                                    
    def update(self, vel_change=None):
        if vel_change:
            vel_change = vel_change.copy()
            
        self.frame_count += 1
        
        while self.frame_count >= 1/self.rate:
            self.frame_count -= 1/self.rate
            self.particles.append(self.get_particle())
                
        i = 0
        while i < len(self.particles):
            particle = self.particles[i]
            invisible = particle.update(vel_change)
            if invisible:
                self.particles.pop(i)
                
    def render(self, surface):
        for particle in self.particles:
            particle.render(surface)
        