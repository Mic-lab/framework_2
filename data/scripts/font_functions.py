import pygame
import os
from pygame.locals import *
from .core_functions import *
from .config import *

def generate_font(font) -> dict:
    images = {}
    font_img = pygame.image.load(f'{font_path}/{font}/{font}.png').convert()
    font_order = open_json(f'{font_path}/{font}/config.json')
    character_count = 0
    last_px = 0
    width = 0
    height = font_img.get_height()
    for px in range(font_img.get_width()):
        color = font_img.get_at((px, 0))
        if color == split_color:
            width = px - width
            character_img = font_img.subsurface(last_px+1, 0, px - last_px, height).convert()
            character_img.set_colorkey(split_color)
            character_img = swap_colors(character_img, split_color, colorkey)
            character_img.set_colorkey(colorkey)
            images[font_order[character_count]] = character_img
            last_px = px
            character_count += 1
    return images

def generate_font_database() -> dict:
    font_database = {}
    fonts = os.listdir(font_path)
    for font in fonts:
        f = os.path.join(font_path, font)
        if not os.path.isfile(f):
            font_database[font] = generate_font(font)
            
    return font_database

def render_line(surf: pygame.Surface, pos: tuple, text: str, characters: dict, CHARACTER_HEIGHT: int, rgb: tuple):
    '''Can only blit a line using a custom font, meaning that "\\n" will be intreperted as part of the line.
    The text will not go passed the surface's width, unless the surface's width is smaller than the width of a word.'''    
    text = text.split(' ')
    
    rendered_text = [[text[0]]]
    line = 0
    for word in text[1:]:
        line_text = rendered_text[line].copy()
        line_text.append(word)
        line_text_width = 0
        for character in ' '.join(line_text):
            line_text_width += characters[character].get_width()
        if line_text_width > surf.get_width() - pos[0]:
            rendered_text.append([])
            line += 1
        rendered_text[line].append(word)
                
    for i, line in enumerate(rendered_text):
        x = 0
        for character in ' '.join(line):
            img = characters[character]
            if rgb != 255:
                img = swap_colors(img, (255, 255, 255), rgb)
            surf.blit(img, (pos[0] + x, pos[1] + (CHARACTER_HEIGHT + 1) * i))
            x += img.get_width()
            
    # The height of the rendered text
    return len(rendered_text)*(CHARACTER_HEIGHT+1)
            
def render_wrapped_text(surf: pygame.Surface, pos: tuple, text: str, characters: dict, rgb: tuple) -> None:
    """Blits text using a custom font. 
    The text will not go passed the surface's width, unless the surface's width is smaller than the width of a word."""    
    # The given character shouldn't matter if every character has the same height
    CHARACTER_HEIGHT = characters[' '].get_height()
    y = 0
    for line in text.split('\n'):
        y += render_line(surf, (pos[0], pos[1] + y), line, characters, CHARACTER_HEIGHT + 1, rgb)
        
def render_text(text: str, characters: dict, rgb: tuple) -> pygame.Surface:
    """Returns a surface of text (Which the custom font given)."""
    CHARACTER_HEIGHT = characters[' '].get_height()
    # The size of the text surface is the canvas's size temporarily.
    # because if the text's dimensions were to exceed this, 
    # it would be too big to go in the canvas in the first place.
    surf = pygame.Surface(CANVAS_SIZE, SRCALPHA)
    x = 0
    for line_count, line in enumerate(text.split('\n')):
        for character in line:
            img = characters[character]
            img = swap_colors(img, (255, 255, 255), rgb)
            surf.blit(img, (x, line_count * CHARACTER_HEIGHT))
            x += img.get_width()
    output = pygame.Surface.subsurface(surf, (0, 0, x, (line_count + 1) * CHARACTER_HEIGHT))
    return output
    # return pygame.Surface.subsurface(surf, (0, 0, x, line_count * CHARACTER_HEIGHT))
    
font_database = generate_font_database()
