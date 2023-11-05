import pygame
from .tank import Tank
from .tankScripts import Inventory
from .inventoryWindow import InventoryWindow



class Player():
    def __init__(self, game, sprite_group, pos):

        # self.tank = Tank(game, sprite_group, pos,'panser2_hull', 'panser2_turret', 'panser2_cannon', 'panser2_barrel', 'test_engine_2')
        self.tank = Tank(game, sprite_group, pos,'T34_hull', 'panser2_turret', '40mm_cannon', 'T34_barrel', 'test_engine_2')

        self.mode = 'tank'
        
        self.inventory = Inventory()
        self.inventory.add_item_by_name('tiger1_hull')
        self.inventory_window = InventoryWindow(self, (500,500), (500,500), 'inv')



        self.click_time = 100
        self.last_click_time = pygame.time.get_ticks() - self.click_time

        self.sight_image = pygame.image.load(f'C:\\Users\\jorba\\PycharmProjects\\RPTank\\assets\\sights\\sight2.png').convert_alpha()
        self.sight_rect = self.sight_image.get_rect(center=(0,0))


    def movement(self, dt, keys, mouse_pos_offset, mouse_pos, mouse_pressed):

        if self.mode == 'tank':
            if keys[pygame.K_d] and keys[pygame.K_w]:
                self.tank.movement(dt, "R_UP")
            elif keys[pygame.K_a] and keys[pygame.K_w]:
                self.tank.movement(dt,"L_UP")

            elif keys[pygame.K_a]:
                self.tank.movement(dt,"LEFT")
            elif keys[pygame.K_d]:
                self.tank.movement(dt,"RIGHT")
            elif keys[pygame.K_w]:
                self.tank.movement(dt,"UP")
            elif keys[pygame.K_s]:
                self.tank.movement(dt,"DOWN")
            else:
                self.tank.movement(dt,"NONE")

            if (keys[pygame.K_SPACE] or mouse_pressed[0]):
                self.tank.shootMainGun()



            self.tank.turretMovement(mouse_pos_offset)




        current_time = pygame.time.get_ticks()

        if current_time - self.last_click_time >= self.click_time:

            if keys[pygame.K_u] and not self.status_window.active:
                self.status_window.active = True
            elif keys[pygame.K_u] and self.status_window.active:
                self.status_window.active = False

            if keys[pygame.K_i] and not self.inventory_window.active:
                self.inventory_window.active = True

            elif keys[pygame.K_i] and self.inventory_window.active:
                self.inventory_window.active = False

            self.last_click_time = current_time



        # self.status_window.move_window(mouse_pos, mouse_pressed)
        self.inventory_window.move_window(mouse_pos, mouse_pressed)
        self.inventory_window.press_button(mouse_pos, mouse_pressed)


    def update_mouse_sight(self, mouse_pos):
        self.sight_rect.center = mouse_pos


    def update(self):
        self.tank.update()


    def draw(self, screen):
        if self.mode == 'tank':
            screen.blit(self.sight_image, self.sight_rect)
        self.inventory_window.draw(screen)




