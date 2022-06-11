from .animations import *
from .core_functions import *
from .config import *

class Entity:
    def __init__(self, pos, type_, offset=[0, 0], friction=0.05, vel=[0, 0], max_vel=2, action='idle', flip=[False, False]):
        self.pos = pos
        self.type = type_
        self.offset = offset
        self.friction = friction
        self.vel = vel
        self.max_vel = max_vel
        self._action = action
        self.action = action
        self.flip = flip
        load_animation(f'{animation_path}/{self.type}')
        self.game_frame = 0
        self.animation_frame = 0

    @property
    def frame_data(self):
        return animation_database[self.type][self.action]['imgs'][int(self.animation_frame)]
    
    @property
    def action(self):
        return self._action
    
    @action.setter
    def action(self, new_action):
        if new_action != self.action:
            self._action = new_action
            self.game_frame = 0
            self.animation_frame = 0
    
    def set_flip(self, new_flip):
        for axis in range(len(new_flip)):
            if new_flip[axis] != self.flip[axis]:
                self.flip[axis] = new_flip[axis]
                if self.flip[axis]:
                    self.pos[axis] -= self.offset[axis]
                else:
                    
                    self.pos[axis] += self.offset[axis]
                
    def update(self):
        
        # Movement ----------------------------------------------------------- #
        for axis in range(2):
            # NOTE: self.vel can be inaccurate at the end but when
            # of the function because friction is applied to it after it  
            # has reached its max it is additioned to self.pos[axis], it  
            # is accurate since we set it to its max before that line
            if self.vel[axis] > self.max_vel:
                self.vel[axis] = self.max_vel
            elif self.vel[axis] < -self.max_vel:
                self.vel[axis] = -self.max_vel
            self.pos[axis] += self.vel[axis]
            if self.vel[axis] > 0:
                self.vel[axis] -= self.friction
                if self.vel[axis] < 0:
                    self.vel[axis] = 0
            else:
                self.vel[axis] += self.friction
                if self.vel[axis] > 0:
                    self.vel[axis] = 0
        
        # Animation ---------------------------------------------------------- #
        self.game_frame += 1
        if self.game_frame > self.frame_data['duration']:
            self.game_frame = 0
            self.animation_frame += 1
            if self.animation_frame >= len(animation_database[self.type][self.action]['imgs']):
                self.animation_frame = 0

    def render(self, surf):
        surf.blit(pygame.transform.flip(self.frame_data['img'], self.flip[0], self.flip[1]), self.pos)