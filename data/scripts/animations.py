from .core_functions import *
from .config import *
import pygame
import json
from os import listdir
from os.path import isdir

entity_animation_database = {}
particle_animation_database = {}

def load_animation(folder, file):
    data = open_json(f'{folder}/config.json')
    output = {
        'sequence': data['sequence'],
        'imgs': []
        }    
    for i, duration in enumerate(data['duration']):
        print(f'Loading {folder}/{file}_{i}.png')
        img = pygame.image.load(f'{folder}/{file}_{i}.png').convert()
        img.set_colorkey(colorkey)                
        output['imgs'].append({'img': img,
                    'duration': duration})
    return output

def load_entity_animation(entity_folder):
    global entity_animation_database

    if entity_folder not in entity_animation_database:
        entity = entity_folder.split('/')[-1]
        entity_animation_database[entity] = {}
        for action in listdir(entity_folder):
            if isdir(f'{entity_folder}/{action}'):
                entity_animation_database[entity][action] = load_animation(f'{entity_folder}/{action}', entity)

def load_particle_animation(particle_folder):
    pass