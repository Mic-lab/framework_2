class AnimationManager:
    
    def __init__(self, animation, animation_frame=0, game_frame=0):
        self._animation = animation
        self.animation_frame = animation_frame
        self.game_frame = game_frame
        
    def update(self):
        self.game_frame += 1
        if self.game_frame > self.animation_data['duration']:
            self.game_frame = 0
            self.animation_frame += 1
            if self.animation_frame >= len(self.animation['imgs']):
                if self.animation['sequence'] == 'loop':
                    self.animation_frame = 0
                else:
                    raise Exception(f'Unsupported sequence "{self.animation["sequence"]}"')
                return True
            
    @property
    def animation(self):
        return self._animation
    
    @animation.setter
    def animation(self, new_animation):
        self._animation = new_animation
        self.animation_frame = 0
        self.game_frame = 0
    
    @property
    def animation_data(self):
        return self.animation['imgs'][self.animation_frame]
                
    @property
    def img(self):
        return self.animation_data['img']