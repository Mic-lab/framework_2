from .core_functions import *
from .config import *
import pygame
import json
from os import listdir
from os.path import isdir

entity_animation_database = {}
particle_animation_database = {}

def load_animation(folder, file, switched_color=None):
    data = open_json(f'{folder}/config.json')
    output = {
        'sequence': data['sequence'],
        'imgs': []
        }    
    for i, duration in enumerate(data['duration']):
        print(f'Loading {folder}/{file}_{i}.png')
        img = pygame.image.load(f'{folder}/{file}_{i}.png').convert()
        if switched_color:
            img = swap_colors(img, (255, 255, 255), switched_color)
        img.set_colorkey(colorkey)                
        output['imgs'].append({'img': img,
                    'duration': duration})
    return output

def load_entity_animation(entity_folder):
    global entity_animation_database
    
    entity = entity_folder.split('/')[-1]
    if entity not in entity_animation_database:
        entity_animation_database[entity] = {}
        for action in listdir(entity_folder):
            if isdir(f'{entity_folder}/{action}'):
                entity_animation_database[entity][action] = load_animation(f'{entity_folder}/{action}', entity)

def load_particle_animation(particle_folder, rgb):
    global particle_animation_database

    file = particle_folder.split('/')[-1]
    particle = f'{file} {rgb}'
    if particle not in particle_animation_database:
        particle_animation_database[particle] = load_animation(particle_folder, file, rgb)        