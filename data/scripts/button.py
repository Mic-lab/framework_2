import colorsys
from copy import deepcopy
from .font_functions import *

class Button:
    presets = {'basic': {'border': [23, 25, 27],
                         'fill': [74, 138, 99],
                         'text': [127, 235, 144],
                         'font': 'basic'}}
    
    presets = {'basic': {
        'colors': {'border': [23, 25, 27], 
                    'fill': [74, 138, 99], 
                    'text': [127, 235, 144]}
                         ,
        'font': 'basic'}
               }
    
    def __init__(self, rect, text, preset):
        self.rect = rect
        self.text = text
        self.preset = preset
        self.selected = False
        self.clicked = False
        self.released = False
        
    @property
    def colors(self):
        if not self.selected:
            return self.presets[self.preset]['colors']
        else:
            if self.clicked:
                change = 0.16
            else:
                change = 0.08

            modes = deepcopy(self.presets[self.preset]['colors'])
                        
            for key, color in modes.items():    
                color = self.rgb_to_hsv(color)
                color[2] += change
                color[1] += change/2
                color[0] -= change/2
                if color[2] > 1:
                    color[2] = 1
                if color[1] > 1:
                    color[1] = 1
                color[0] = color[0] % 1
                color = self.hsv_to_rgb(color)
                modes[key] = color
            return modes

        
    def update(self, mx, my, mouse_down, clicked):
        if self.rect.collidepoint(mx, my):
            self.selected = True
            if clicked:
                self.clicked = True
            if not(self.clicked and mouse_down):
                self.clicked = False
        else:
            self.selected = False
            self.clicked = False

            if clicked and not mouse_down:
                self.clicked = False
        
                
    def render(self, surf):
        pygame.draw.rect(surf, self.colors['border'], self.rect, border_radius=2)
        x, y, w, h = self.rect
        x += 1
        y += 1
        w -= 2
        h -= 3
        pygame.draw.rect(surf, self.colors['fill'], (x, y, w, h), border_radius=2)
        pygame.draw.aaline(surf, self.colors['text'], (x, y), (x, y + h - 2))
        pygame.draw.aaline(surf, self.colors['text'], (x, y), (x + w - 1, y))
        text_img = render_text(self.text, font_database[self.presets[self.preset]['font']], self.colors['text'])
        center_blit([(self.rect.x * 2 + self.rect.width, self.rect.y * 2+ self.rect.height), text_img], surf)
        return text_img
    
    @staticmethod
    def rgb_to_hsv(rgb):
        small_rgb = [i/255 for i in rgb]
        return list(colorsys.rgb_to_hsv(*small_rgb))
    
    @staticmethod
    def hsv_to_rgb(hsv):
        hsv = list(colorsys.hsv_to_rgb(*hsv))
        return [i*255 for i in hsv]