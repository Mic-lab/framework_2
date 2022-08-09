import json
import pygame
from math import atan, pi

def open_txt(path):
    with open(path, 'r') as f:
        data = f.read()
    return data

def open_json(path):
    data = open_txt(path)
    return json.loads(data)

def swap_colors(surface, color_1, color_2):
    surface_copy = surface.copy()
    output_surface = surface.copy()
    output_surface.fill(color_2)
    surface_copy.set_colorkey(color_1)
    output_surface.blit(surface_copy, (0, 0))
    return output_surface

def get_center_pos(coordinates) -> tuple:
    return (coordinates[0][0] / 2 - coordinates[1][0] / 2,
            coordinates[0][1] / 2 - coordinates[1][1] / 2)
    
def center_blit(coordinates:list, dest: pygame.Surface=None) -> None:
    """Blits a surface in center of another surface.
    
    Keyword arguments:
    coordinates -- list of length two, containing rather a coordinate (tuple) or a pygame.Surface
    dest -- pygame.Surface
    
    Second item in coordinates is the dest by default
    """
    coordinates_copy = coordinates.copy()
    
    if dest is None:
        dest = coordinates_copy[0]
        
    for i, coordinate in enumerate(coordinates_copy):
        if isinstance(coordinate, pygame.Surface):
            coordinates_copy[i] = coordinate.get_size()
            
    dest.blit(coordinates[1], get_center_pos(coordinates_copy))
    
def get_angle(vector):
    angle = atan(vector[1] / vector[0]) * 180 / pi + 90
    if vector[0] < 0:
        angle -= 180
    return angle
    