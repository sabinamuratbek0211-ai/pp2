import pygame
from clock import MickeyClock

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

WHITE = (255, 255, 255)

clock_obj = MickeyClock(screen)

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock_obj.draw()

    pygame.display.flip()
    clock.tick(1)  

pygame.quit()