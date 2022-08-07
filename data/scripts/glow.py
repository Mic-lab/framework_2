import pygame
from pygame.locals import *

class Glow:
    
    def __init__(self, colors, radius, alphas):
        """All arguments must have the same length since each one corresponds to
        a seperate glow"""
        self.colors = colors
        self.radius = radius
        self.alphas = alphas
        
    @property
    def surfs(self):
        surfs = []
        for i, color in enumerate(self.colors):
            surf = pygame.Surface((self.radius[i] * 2, self.radius[i] * 2))
            pygame.draw.circle(surf, color, (self.radius[i], self.radius[i]), self.radius[i])
            surf.set_colorkey((0, 0, 0))
            surfs.append(surf)
        return surfs
            
    def render(self, surface, pos, center=True, special_flag=BLEND_RGB_ADD):
        for i, surf in enumerate(self.surfs):
            if center:
                surface.blit(surf, (pos[0] - self.radius[i], pos[1] - self.radius[i]), special_flags=special_flag)
            else:
                surface.blit(surf, pos, special_flags=special_flag)