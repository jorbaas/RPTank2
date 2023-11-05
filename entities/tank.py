from .parts import *
from entities.tankScripts import *
from .effects import *

import pygame
from .item import Item


class Tank(pygame.sprite.Sprite, TankMovement):
    def __init__(self, game, sprite_group, pos, hull_name, turret_name, cannon_name, barrel_name, engine_name):
        super().__init__(sprite_group)
        # instance of game to call methods
        self.game = game
        # name for the sprite
        self.name = 'tank'



        # tank is build of these objects
        self.turret = Turret(turret_name, pos)
        self.barrel = Barrel(self.turret, barrel_name, pos)
        self.hull = Hull(hull_name, pos)
        self.engine = Engine(engine_name)
        self.cannon = Cannon(cannon_name)

        self.equipped_parts = [Item(self.barrel.name, 'barrel'),
                               Item(self.turret.name, 'turret'),
                               Item(self.hull.name, 'hull'),
                               Item(self.engine.name, 'engine'),
                               Item(self.cannon.name, 'cannon')]


        # set the turret and barrel offset
        self.turret.calculate_turret_offset(self.hull.rect, self.hull.turret_offset, self.hull.angle)
        self.barrel.calculate_barrel_offset(self.turret.rect, self.turret.barrel_offset, self.turret.angle)

        # total mass of the tanks
        self.mass = self.hull.mass + self.turret.mass + self.barrel.mass + self.engine.mass + self.cannon.mass

        self.health = 100
        self.acceleration = self.calculateAcceleration(self.mass, self.engine.power)
        self.speed = 0
        self.angle = self.hull.angle

        # for smoke effects etc
        self.particles = []
        self.flashes = []


        # ammo stuff
        self.allowed_caliber = self.cannon.caliber
        self.ammo_storage = {'AP_40': 99, 'HE_40': 99}
        self.active_ammo = 'AP_40'


        self.aim_loc = (0,0)

        self.shooting_speed = self.cannon.shooting_speed * 1000
        self.last_shot_time = pygame.time.get_ticks() - self.shooting_speed

        self.rect = self.hull.rect
        self.pos = pygame.math.Vector2(self.rect.center)
        self.velocity = pygame.math.Vector2()
        self.mask = pygame.mask.from_surface(self.hull.image)
        self.front_mask = pygame.mask.from_surface(self.hull.image_hitbox_front)
        self.right_mask = pygame.mask.from_surface(self.hull.image_hitbox_right)
        self.left_mask = pygame.mask.from_surface(self.hull.image_hitbox_left)
        self.rear_mask = pygame.mask.from_surface(self.hull.image_hitbox_rear)

        self.hitbox_image = pygame.image.load('assets/images/parts/hulls/T34_hull_hitbox.png')
        self.hitbox_rect = self.hitbox_image.get_rect(center=self.rect.center)
        self.target_lock = True
        self.colliding = False
        self.player = False


    def movement(self, dt, direction):
        max_speed = self.engine.max_speed

        if direction == "R_UP":
            if self.speed <= max_speed:
                self.speed += self.acceleration * 0.5
            self.hull.angle -= 1
            self.turret.angle -= 1

        elif direction == "L_UP":
            if self.speed <= max_speed:
                self.speed += self.acceleration * 0.5

            self.hull.angle += 1
            self.turret.angle += 1

        elif direction == "UP":
            if self.speed <= max_speed:
                self.speed += self.acceleration

        elif direction == "DOWN":
            if self.speed >= -max_speed:
                self.speed -= self.acceleration

        elif direction == "RIGHT":
            self.speed = self.calcualteSpeed(self.speed, self.acceleration)
            self.hull.angle -= 1
            self.turret.angle -= 1

        elif direction == "LEFT":
            self.speed = self.calcualteSpeed(self.speed, self.acceleration)
            self.hull.angle += 1
            self.turret.angle += 1

        if direction == "NONE":
            if self.speed > 0:
                self.speed = max(0, self.speed - self.acceleration)

            elif self.speed < 0:
                self.speed = max(0, self.speed - self.acceleration)

        self.calculateMovent(dt)
        self.turret.calculate_turret_offset(self.hull.rect, self.hull.turret_offset, self.hull.angle)
        self.barrel.calculate_barrel_offset(self.turret.rect, self.turret.barrel_offset, self.turret.angle)


    def turretMovement(self, mouse_pos, rotation_speed=1):
        # Calculate the angle to rotate the turret to point at the player
        turret_center = self.turret.rect.center

        dx = mouse_pos[0] - turret_center[0]
        dy = mouse_pos[1] - turret_center[1]

        self.aim_loc = mouse_pos

        # Calculate the angle in degrees
        target_angle = math.degrees(math.atan2(-dy, dx)) - 90

        # Gradually rotate the turret towards the target angle
        angle_difference = (target_angle - self.turret.angle) % 360

        if angle_difference > 180:
            angle_difference -= 360

        if angle_difference < -180:
            angle_difference += 360

        # Calculate the maximum rotation amount based on rotation_speed
        max_rotation = rotation_speed  # Adjust this value for the desired rotation speed

        if abs(angle_difference) > max_rotation:
            if angle_difference > 0:
                self.turret.angle += max_rotation
                self.target_lock = False
            else:
                self.turret.angle -= max_rotation
                self.target_lock = False
        elif not self.target_lock:
            self.turret.angle = target_angle
            self.target_lock = True

        self.barrel.calculate_barrel_offset(self.turret.rect, self.turret.barrel_offset, self.turret.angle)


    def switchPart(self, part_name, type):
        pos = (self.rect.centerx, self.rect.centery)
        if type == 'hull':
            self.hull = Hull(part_name, pos, self.angle)
        elif type == 'turret':
            self.turret = Turret(part_name, pos)
            self.barrel.turret = self.turret
        elif type == 'barrel':
            self.barrel = Barrel(self.turret, part_name, pos)

        elif type == 'cannon':
            self.cannon = Cannon(part_name)
            self.shooting_speed = self.cannon.shooting_speed * 1000
            self.allowed_caliber = self.cannon.caliber

        elif type == 'engine':
            self.engine = Engine(part_name)

        self.equipped_parts = [Item(self.barrel.name, 'barrel'),
                               Item(self.turret.name, 'turret'),
                               Item(self.hull.name, 'hull'),
                               Item(self.engine.name, 'engine'),
                               Item(self.cannon.name, 'cannon')]

        self.mass = self.hull.mass + self.turret.mass + self.barrel.mass + self.engine.mass + self.cannon.mass
        self.acceleration = self.calculateAcceleration(self.mass, self.engine.power)

    def muzzle_flash(self):
        start_pos = calculateAngleOffset(self.barrel.rect, self.turret.angle, self.barrel.fire_offset)
        self.flashes.append(Flash(start_pos[0], start_pos[1], 10))

        particle = Smoke((start_pos[0], start_pos[1]), 2, 30, self.turret.angle, 160, 0.2, 0.03)
        self.particles.append(particle)

        if self.barrel.muzzle_break == 1:
            particle2 = Smoke((start_pos[0], start_pos[1]), 2, 10, self.turret.angle + 90, 120, 0.2,
                              0.025)
            particle3 = Smoke((start_pos[0], start_pos[1]), 2, 10, self.turret.angle - 90, 120, 0.2,
                              0.025)
            self.particles.append(particle2)
            self.particles.append(particle3)

    def shootMainGun(self):

        if self.ammo_storage[self.active_ammo] > 0:

            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.shooting_speed:
                # start pos of the bullet
                start_pos = calculateAngleOffset(self.barrel.rect, self.turret.angle, self.barrel.fire_offset)

                if self.target_lock: # shoots directly at the cursor if aligned
                    self.game.create_bullet(start_pos, self.aim_loc, self.turret.angle, self.active_ammo, locked=True)
                else: # shoots from the turret angle if not aligned with the cursor
                    self.game.create_bullet(start_pos, self.aim_loc, self.turret.angle, self.active_ammo, locked=False)

                self.muzzle_flash()
                self.last_shot_time = current_time


    def update(self):

        self.hull.fuel_amount = self.calculate_fuel(self.hull.fuel_amount, self.mass, self.engine.power, self.speed)

        for particle in self.particles:
            particle.update()

        for flash in self.flashes:
            flash.update()

        self.rect = self.hull.rect
        self.hitbox_rect = self.hull.rect
        self.angle = self.hull.angle

        # update parts
        self.hull.update()
        self.turret.update()
        self.barrel.update()

        self.tank_mask = pygame.mask.from_surface(self.hull.image)
        self.front_mask = pygame.mask.from_surface(self.hull.image_hitbox_front)
        self.right_mask = pygame.mask.from_surface(self.hull.image_hitbox_right)
        self.left_mask = pygame.mask.from_surface(self.hull.image_hitbox_left)
        self.rear_mask = pygame.mask.from_surface(self.hull.image_hitbox_rear)










