import pygame
import sys

pygame.init()

# Screen settings
WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)

# Current drawing settings
color = BLUE
radius = 8
mode = "brush"

# Canvas background
screen.fill(WHITE)

drawing = False
start_pos = None


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # Color selection
            if event.key == pygame.K_r:
                color = RED
            elif event.key == pygame.K_g:
                color = GREEN
            elif event.key == pygame.K_b:
                color = BLUE
            elif event.key == pygame.K_k:
                color = BLACK

            # Tool selection
            elif event.key == pygame.K_1:
                mode = "brush"
            elif event.key == pygame.K_2:
                mode = "rectangle"
            elif event.key == pygame.K_3:
                mode = "circle"
            elif event.key == pygame.K_4:
                mode = "eraser"

            # Change brush size
            elif event.key == pygame.K_UP:
                radius += 2
            elif event.key == pygame.K_DOWN:
                radius = max(2, radius - 2)

        # Mouse press
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        # Mouse release
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            # Draw rectangle after releasing mouse
            if mode == "rectangle":
                x1, y1 = start_pos
                x2, y2 = end_pos
                rect = pygame.Rect(min(x1, x2), min(y1, y2),
                                   abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, color, rect, 3)

            # Draw circle after releasing mouse
            elif mode == "circle":
                x1, y1 = start_pos
                x2, y2 = end_pos
                circle_radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, circle_radius, 3)

        # Mouse movement for brush and eraser
        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "brush":
                pygame.draw.circle(screen, color, event.pos, radius)

            elif mode == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, radius)

    pygame.display.update()
    clock.tick(60)