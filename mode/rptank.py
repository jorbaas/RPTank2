import pygame
from settings import BLACK
import math
from camera import CameraGroup, HUD
from entities.effects import Explosion
from entities import  *
from enemy import EnemySimple
from .gameScripts import GameScripts


class RPTank(GameScripts):
    def __init__(self):
        self.camera_group = CameraGroup()

        self.player = Player(self, self.camera_group, (300,300))

        self.enemies = [EnemySimple(self, self.camera_group, (300, 500))]



        self.hud = HUD(self.player)

        self.bullets = []
        self.explosions = []

        pygame.mouse.set_visible(False)
        self.ground_mask = pygame.mask.from_surface(self.camera_group.ground_image)
        self.ground_overlay_mask = pygame.mask.from_surface(self.camera_group.ground_collision_image)




    def input(self, dt):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        offset = self.offset_mouse_pos()

        mouse_pos_offset = ((mouse_pos[0] + offset[0]), (mouse_pos[1] + offset[1]))

        self.player.movement(dt, keys, mouse_pos_offset, mouse_pos, mouse_pressed)
        self.player.update_mouse_sight(mouse_pos)



    def offset_mouse_pos(self):
        offset = (self.player.tank.rect.centerx - 800), (self.player.tank.rect.centery - 450)
        return offset

    def create_bullet(self, pos, target_pos, angle, name = 'AP_40', locked=True):
        bullet = Bullet(self.camera_group, self, pos, target_pos, angle, name, locked)
        if bullet.caliber == self.player.tank.cannon.caliber:
            self.bullets.append(bullet)


    def create_explosion(self, rect, size, type):
        "Explosion is created if bullet is not alive"
        explosion = Explosion(self.camera_group, rect, size)
        if type == 'AP':
            explosion.small_impact()
            self.explosions.append(explosion)
        elif type == 'HE':
            explosion.he_small_explosion()
            self.explosions.append(explosion)


    def collision(self, dt):
        # collision with ground alpha and ground_collision_overlay
        pos = (self.player.tank.rect.x, self.player.tank.rect.y)
        self.player.tank.colliding = False
        if not self.ground_mask.overlap(self.player.tank.mask, pos) or self.ground_overlay_mask.overlap(self.player.tank.mask, pos):
            self.player.tank.handleCollision(dt)
            self.player.tank.colliding = True

        for enemy in self.enemies:
            if enemy.tank.hitbox_rect.colliderect(self.player.tank.hitbox_rect):
                self.player.tank.handleCollision(dt)
                self.player.tank.colliding = True

        # bullet collisions
        for bullet in self.bullets:
            hit = None
            hit_enemy = None
            # with enemies
            for enemy in self.enemies:
                pos = (bullet.rect.x - enemy.tank.rect.x, bullet.rect.y - enemy.tank.rect.y)


                if enemy.tank.front_mask.overlap(bullet.mask, pos):
                    hit = 'front'
                    hit_enemy = enemy
                    break
                elif enemy.tank.right_mask.overlap(bullet.mask, pos):
                    hit = 'right'
                    hit_enemy = enemy
                    break
                elif enemy.tank.left_mask.overlap(bullet.mask, pos):
                    hit = 'left'
                    hit_enemy = enemy
                    break
                elif enemy.tank.rear_mask.overlap(bullet.mask, pos):
                    hit = 'rear'
                    hit_enemy = enemy
                    break
            if hit != None:
                self.damage_calculation(bullet, hit_enemy, hit)
                bullet.alive = False


            # with the world collision overlay
            if self.ground_overlay_mask.overlap(bullet.mask, bullet.rect.center):
                bullet.alive = False


    def update(self, dt):
        self.player.update()
        for enemy in self.enemies:
            enemy.update(dt)

        for bullet in self.bullets:
            bullet.update()
            if not bullet.alive:
                self.create_explosion(bullet.rect.center, bullet.radius, bullet.explosion_type)
                self.bullets.remove(bullet)
                self.camera_group.remove(bullet)

        for explosion in self.explosions:
            explosion.update()

        self.collision(dt)
        self.hud.update()

    def draw(self, screen, dt):
        screen.fill('blue')

        self.camera_group.custom_draw(self.player.tank, dt)
        self.player.draw(screen)
        self.hud.draw(screen)

    def run(self, screen, dt):
        self.input(dt)
        self.update(dt)

        self.draw(screen, dt)