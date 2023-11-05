import pygame
import math
from .itemValues import *
from .item import Item


def calculateAngleOffset(start_rect, angle, offset):
    direction_vector = pygame.math.Vector2(0, 1)
    rotated_vector = direction_vector.rotate(-angle)
    end_position = start_rect.center + rotated_vector * offset
    return end_position


class Inventory():
    def __init__(self):

        # {'item1': [item, amount]}
        self.items = {}
        self.ammo = {}

    def add_item(self, item, amount=1):

        if item.values['name'] in self.items and item.type != 'ammo':
            self.items[item.values['name']][1] += amount
        elif item.type != 'ammo':
            self.items[item.values['name']] = [item, amount]
        elif item.values['name'] in self.ammo and item.type == 'ammo':
            self.ammo[item.values['name']][1] += amount

        elif item.type == 'ammo':

            self.ammo[item.values['name']] = [item, amount]


    def add_item_by_name(self, name, amount=1):
        items = [all_cannons, all_engines, all_barrels, all_hulls, all_turrets, all_ammo]
        for item_dict in items:
            if name in item_dict:
                item = Item(name, item_dict[name]['type'])
                self.add_item(item, amount)


    def remove_item(self, item, amount=1):
        if item.values['name'] in self.items:
            self.items[item.values['name']][1] -= amount
            if self.items[item.values['name']][1] <= 0:
                self.items.pop(item.values['name'])
        elif item.values['name'] in self.ammo:
            self.ammo[item.values['name']][1] -= amount
            if self.ammo[item.values['name']][1] <= 0:
                self.ammo.pop(item.values['name'])



class TankMovement():

    def __init__(self):
        self.hull_rect = None
        self.pos = None
        self.hull_angle = None
        self.angle = None
        self.barrel = None
        self.turret = None
        self.hull = None
        self.velocity = None
        self.speed = None

    def calculateMovent(self, dt):
        # Calculate the horizontal and vertical components of the movement
        movement_angle = math.radians(-self.angle%360)
        self.pos.x += self.speed * math.sin(movement_angle) * dt
        self.pos.y -= self.speed * math.cos(movement_angle) * dt # Negative because pygame's y-axis is inverted


        # Update the tank's position


        self.hull.rect.centerx = self.pos.x
        self.hull.rect.centery = self.pos.y

        self.turret.rect.centerx = self.pos.x
        self.turret.rect.centery = self.pos.y

        self.barrel.rect.centerx = self.pos.x
        self.barrel.rect.centery = self.pos.y




    def calculateAcceleration(self, mass, power):
        acceleration = power / (mass*1000)
        return acceleration


    def calculate_fuel(self, fuel, mass, power, speed):
        usage = power * speed / (mass * 5000)
        fuel -= usage
        return fuel


    def calculateTurretAngle(self, mouse_pos, turret_rect):
        # Calculate the vector from the turret's position to the player's position
        dx = mouse_pos[0] - turret_rect.centerx
        dy = mouse_pos[1] - turret_rect.centery

        # Calculate the angle in radians between the turret's direction and the player
        turret_angle = math.atan2(-dy, dx)  # The negative dy is because the y-axis is often inverted in games

        # Convert the angle from radians to degrees (optional, depends on your angle units)
        turret_angle = math.degrees(turret_angle) - 90

        return turret_angle


    def calcualteSpeed(self, speed, acceleration):
        if speed > 0:
            speed = max(0, speed - acceleration)
        elif speed < 0:
            speed = max(0, speed - acceleration)
        return speed


    def calculateDistance(self, pos1, pos2):
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        distance = math.sqrt(dx * dx + dy * dy)
        return distance

    def calculateAngle(self, pos1, pos2):
        angle = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])
        angle = math.degrees(angle)
        return angle%360




    def handleCollision(self, dt):
        # if self.speed > 0:
        #     self.speed = -1
        #     self.calculateMovent(dt)
        # elif self.speed <= 0:
        #     self.speed = 1
        #     self.calculateMovent(dt)
        self.speed = 0




