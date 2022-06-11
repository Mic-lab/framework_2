from .core_functions import *
from .config import *
import pygame
import json
from os import listdir

animation_database = {}

def load_animation(entity_folder):
    global animation_database

    entity = entity_folder.split('/')[-1]
    animation_database[entity] = {}
    for action in listdir(entity_folder):
        # Check's if it's a folder
        if len(action.split('.')) == 1:
            data = open_json(f'{entity_folder}/{action}/config.json')
            animation_database[entity][action] = {
                'sequence': data['sequence'],
                'imgs': []
                }
            imgs = animation_database[entity][action]['imgs']
            # TODO: Implement sequence control
            for i, duration in enumerate(data['duration']):
                print(f'{entity_folder}/{action}/{entity}_{i}.png')
                img = pygame.image.load(f'{entity_folder}/{action}/{entity}_{i}.png').convert()
                img.set_colorkey(colorkey)                
                imgs.append({'img': img,
                             'duration': duration})
