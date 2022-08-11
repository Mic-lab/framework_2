import pygame
from .animated_particle import AnimatedParticle
from .movable_object import MovableObject
from random import uniform

# NOTE: This AnimatedParticleGenerator and Particle Generator 
# have a lot of similar code
class AnimatedParticleGenerator(MovableObject):
        
    def __init__(self, rate, rate_randomness, vel_randomness, pos, vel, friction, type_, rgb, max_vel=None, duration=None, randomize_particle_duration=True):
        self.rate = rate # Target rate
        self.randomized_rate = rate
        self.rate_randomness = rate_randomness
        # If rate - rate_randomness is near 0, this can create some very slow
        # particles. Which is why it's not recommended. 
        self.vel_randomness = vel_randomness
        self.duration = duration
        self.particles = []
        self.frame_count = 0
        self.randomize_particle_duration = randomize_particle_duration
        
        super().__init__(pos, vel, friction, max_vel)
        self.type = type_
        self.rgb = rgb

    def get_particle(self):
        vel = [self.apply_random_change(self.vel[0], self.vel_randomness[0], 1),
                self.apply_random_change(self.vel[1], self.vel_randomness[1], 1)]
        return AnimatedParticle(self.pos.copy(), vel, self.friction, self.type, self.rgb, self.randomize_particle_duration, max_vel=self.max_vel)
        
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