class AnimationManager:
    
    def __init__(self, animations, animation_frame=0, game_frame=0):
        self.animations = animations
        self.animation_frame = animation_frame
        self.game_frame = game_frame
        
    def update(self):
        self.game_frame += 1
        if self.game_frame > self.animation_data['duration']:
            self.game_frame = 0
            self.animation_frame += 1
            if self.animation_frame >= len(entity_animation_database[self.type][self.action]['imgs']):
                if self.animations['sequence'] == 'loop':
                    self.animation_frame = 0
                else:
                    raise Exception(f'Unsupported sequence "{self.animations["sequence"]}"')
                return True
    
    @property
    def animation_data(self):
        return self.animations['imgs'][self.animation_frame]
                
    @property
    def img(self):
        self.animation_data['img']