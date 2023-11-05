import pygame


class ProgressBar():
    def __init__(self, pos, size, color, value, max):
        self.pos = pos
        self.size = size
        self.value = value
        self.max = max
        self.color = color

        self.rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])
        self.bar_rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])


    def calc_bar_size(self, value):
        self.bar_rect.height = (value / self.max) * self.size[1]
        # increase the y of the bar so it goes down with the height decrease
        self.bar_rect.y = self.pos[1] + (self.size[1] - (value / self.max) * self.size[1])

    def update(self, value):
        self.calc_bar_size(value)


    def draw(self, screen):

        pygame.draw.rect(screen, 'grey', self.rect)
        pygame.draw.rect(screen, self.color, self.bar_rect)




class HUD():
    def __init__(self, player):
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 16)
        self.player = player

        self.slot_image = pygame.image.load('assets/item_slot.png').convert_alpha()

        self.fuel_meter = ProgressBar((10,100), (20, 200), 'brown', 80, 100)








    def update(self):
        if self.player.tank.speed > 0:
            self.fuel_meter.calc_bar_size(self.player.tank.hull.fuel_amount)

    def draw(self, screen):


        self.fuel_meter.draw(screen)
