import pygame

pygame.init()
font = pygame.font.Font(None, 30)

def debug(text, y=10, x=10):
    display = pygame.display.get_surface()
    debug_surf = font.render(str(text), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display, 'black', debug_rect)
    display.blit(debug_surf, debug_rect)