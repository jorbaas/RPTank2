import pygame
import math
from .itemValues import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprite_group, game, pos, target_pos, angle, bullet_name, locked):
        super().__init__(sprite_group)

        self.game = game
        # location of where the bullet needs to travel to
        self.target_pos = target_pos
        self.angle = angle

        self.values = all_ammo[bullet_name]
        self.bullet_name = bullet_name
        self.caliber = self.values['caliber']
        self.radius = self.values['radius']
        self.explosion_type = self.values['explosion_type']
        self.speed = 10  # maybe set it in bullet values
        self.damage = self.values['damage']

        # values for sorting the render
        self.name = 'bullet'
        self.type = 'ammo'

        self.image = pygame.image.load(f'assets/images/ammo/{self.values["image_name"]}.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))
        self.mask = pygame.mask.from_surface(self.image)

        self.alive = True
        self.locked = locked



    def update(self):
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        if self.locked:
            self.angle = math.degrees(math.atan2(dy, dx))
            self.rect.x += self.speed * math.cos(math.radians(self.angle))
            self.rect.y += self.speed * math.sin(math.radians(self.angle))

        else:
            # Update the bullet's velocity based on the calculated angle
            self.rect.x -= self.speed * math.sin(math.radians(self.angle))
            self.rect.y -= self.speed * math.cos(math.radians(self.angle))

        # Check if the bullet has reached the target position
        if math.hypot(dx, dy) < self.speed:
            self.alive = False



