import pygame
from .itemValues import *


class Item():
    def __init__(self, name, type):

        self.name = name
        self.type = type

        self.setup()

        self.rect = None


    def setup(self):
        if self.type == 'hull':
            self.values = all_hulls[self.name]
            self.image = pygame.image.load(f'assets/images/items/hulls/{self.values["image_name"]}.png')
            self.rect = self.image.get_rect()
        elif self.type == 'turret':
            self.values = all_turrets[self.name]
            self.image = pygame.image.load(f'assets/images/items/turrets/{self.values["image_name"]}.png')
            self.rect = self.image.get_rect()
        elif self.type == 'barrel':
            self.values = all_barrels[self.name]
            self.image = pygame.image.load(f'assets/images/items/barrels/{self.values["image_name"]}.png')
            self.rect = self.image.get_rect()
        elif self.type == 'engine':
            self.values = all_engines[self.name]
            self.image = pygame.image.load(f'assets/images/items/engines/{self.values["image_name"]}.png')
            self.rect = self.image.get_rect()
        elif self.type == 'cannon':
            self.values = all_cannons[self.name]
            self.image = pygame.image.load(f'assets/images/items/cannons/{self.values["image_name"]}.png')
            self.rect = self.image.get_rect()
        elif self.type == 'ammo':
            self.values = all_ammo[self.name]
            self.image = pygame.image.load(f'assets/images/items/ammo/{self.values["image_name"]}.png')
            self.rect = self.image.get_rect()