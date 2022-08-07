import pygame
from .particle import *
from .movable_object import *

class ParticleGenerator(MovableObject):
    
    def __init__(self, rate, rate_randomness, random_change, vel_randomness, pos, vel, friction, initial_img, alpha, changed_alpha, changed_size, glow, angle_at_vel=False, max_vel=None, size=1, duration=None, center=True):
        self.rate = rate # Target rate
        self.randomized_rate = rate
        self.rate_randomness = rate_randomness
        # If rate - rate_randomness is near 0, this can create some very slow
        # particles. Which is why it's not recommended. 
        self.duration = duration
        self.particles = []
        self.frame_count = 0
            
        # Particle attributes
        self.random_change = random_change
        self.vel_randomness = vel_randomness
        super().__init__(pos, vel, friction, max_vel)
        self.initial_img = initial_img
        if initial_img:
            self.initial_img = initial_img.convert()
            self.initial_img.set_colorkey(colorkey)
        self.size = size
        self.changed_size = changed_size
        self.alpha = alpha
        self.changed_alpha = changed_alpha
        self.glow = glow
        self.center = center
        self.angle_at_vel = angle_at_vel
        
    def get_particle(self):
        return Particle(self.random_change, self.vel_randomness.copy(), self.pos.copy(), self.vel.copy(), self.friction, self.initial_img, self.alpha, self.changed_alpha, self.changed_size, self.glow, angle_at_vel=self.angle_at_vel, max_vel=self.max_vel, size=self.size, center=self.center)
        
    def update_and_render(self, surface, vel_change=None):
        """This function updates and renders, instead of doing both of those
        methods seperatly. This is preferable then calling both methods together
        because I don't need to iterate through particles twice, which will be less effecient
        when it comes to performance.
        """
        if vel_change:
            vel_change = vel_change.copy()
            
        self.frame_count += 1
        
        creating_particle = False
        while self.frame_count >= 1/self.randomized_rate:
            creating_particle = True
            self.frame_count -= 1/self.rate
            self.particles.append(self.get_particle())
            
        if creating_particle:
            self.randomized_rate = self.apply_random_change(self.rate, self.rate_randomness, 1)
            
        i = 0
        while i < len(self.particles):
            particle = self.particles[i]
            invisible = particle.update(vel_change)
            if invisible:
                self.particles.pop(i)
            else:
                particle.render(surface)
                i += 1
                
        if self.duration is not None:
            if self.duration > 1:
                self.duration -= 1
                return False
            else:
                return True
        else:
            return False
          
    def update(self, vel_change=None):
        if vel_change:
            vel_change = vel_change.copy()
            
        self.frame_count += 1
        
        creating_particle = False
        while self.frame_count >= 1/self.randomized_rate:
            creating_particle = True
            self.frame_count -= 1/self.rate
            self.particles.append(self.get_particle())
            
        if creating_particle:
            self.randomized_rate = self.apply_random_change(self.rate, self.rate_randomness, 1)
            
        i = 0
        while i < len(self.particles):
            particle = self.particles[i]
            invisible = particle.update(vel_change)
            if invisible:
                self.particles.pop(i)
            else:
                i += 1
                
        if self.duration is not None:
            if self.duration > 1:
                self.duration -= 1
                return False
            else:
                return True
        else:
            return False
                
    def render(self, surface):
        for particle in self.particles:
            particle.render(surface)
        
    # NOTE: This method is copy pasted from particle.py
    @staticmethod
    def apply_random_change(target_attribute, changed_attribute, randomness):
        min_value = target_attribute - changed_attribute * randomness
        max_value = target_attribute + changed_attribute * randomness
        return uniform(min_value, max_value)