from .animations import entity_animation_database, load_entity_animation
from .core_functions import *
from .config import *
from .movable_object import MovableObject

class Entity(MovableObject):
    def __init__(self, pos, type_, offset=[0, 0], friction=0.06, vel=[0, 0], max_vel=None, action='idle', flip=[False, False]):
        super().__init__(pos, vel, friction, max_vel)
        self.type = type_
        self.offset = offset
        self._action = action
        self.action = action
        self.flip = flip
        load_entity_animation(f'{animation_path}/{self.type}')
        self.game_frame = 0
        self.animation_frame = 0

    @property
    def frame_data(self):
        return entity_animation_database[self.type][self.action]['imgs'][int(self.animation_frame)]
    
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

        # Mouvement ---------------------------------------------------------- #
        super().update()
        
        # Animation ---------------------------------------------------------- #
        self.game_frame += 1
        if self.game_frame > self.frame_data['duration']:
            self.game_frame = 0
            self.animation_frame += 1
            if self.animation_frame >= len(entity_animation_database[self.type][self.action]['imgs']):
                self.animation_frame = 0

    def render(self, surf):
        surf.blit(pygame.transform.flip(self.frame_data['img'], self.flip[0], self.flip[1]), self.pos)