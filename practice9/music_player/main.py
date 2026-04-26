import pygame
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

playlist = [
    "music/track1.wav",
    "music/track2.wav"
]

player = MusicPlayer(playlist)

running = True

while running:
    screen.fill(WHITE)

    title = font.render("Music Player", True, BLACK)
    controls1 = font.render("P-Play  S-Stop", True, BLACK)
    controls2 = font.render("N-Next  B-Back  Q-Quit", True, BLACK)
    current = font.render(f"Current: {player.playlist[player.current]}", True, BLACK)

    screen.blit(title, (200, 50))
    screen.blit(controls1, (150, 150))
    screen.blit(controls2, (120, 200))
    screen.blit(current, (80, 280))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.prev()
            elif event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()

