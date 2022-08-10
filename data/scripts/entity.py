from .animations import entity_animation_database, load_entity_animation
from .core_functions import *
from .config import *
from .movable_object import MovableObject
from .animation_manager import AnimationManager

class Entity(MovableObject):

    def __init__(self, pos, type_, offset=[0, 0], friction=0.06, vel=[0, 0], max_vel=None, action='idle', flip=[False, False]):
        super().__init__(pos, vel, friction, max_vel)
        load_entity_animation(f'{animation_path}/{type_}')        
        self.type = type_
        self.offset = offset
        self.set_action(action, True)
        self.flip = flip

    # TODO: Add setter for when type changes
    def set_action(self, new_action, force_changes=False):            
        if force_changes or new_action != self.action:
            self.action = new_action
            self.animation_manager = AnimationManager(entity_animation_database[self.type][new_action])
    
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
        self.animation_manager.update()

    def render(self, surf):
        surf.blit(pygame.transform.flip(self.animation_manager.img, self.flip[0], self.flip[1]), self.pos)