import pygame
import sys
import math

pygame.init()

# Screen settings
WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 16)

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

# Background
screen.fill(WHITE)

drawing = False
start_pos = None


# === Инструкция на экран ===
def draw_instructions():
    instructions = [
        "1 - Brush",
        "2 - Rectangle",
        "3 - Circle",
        "4 - Eraser",
        "5 - Square",
        "6 - Right Triangle",
        "7 - Equilateral Triangle",
        "8 - Rhombus",
        "R/G/B/K - Colors",
        "UP/DOWN - Size"
    ]

    y = 10
    for line in instructions:
        text = font.render(line, True, BLACK)
        screen.blit(text, (450, y))
        y += 18


while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # Colors
            if event.key == pygame.K_r:
                color = RED
            elif event.key == pygame.K_g:
                color = GREEN
            elif event.key == pygame.K_b:
                color = BLUE
            elif event.key == pygame.K_k:
                color = BLACK

            # Modes
            elif event.key == pygame.K_1:
                mode = "brush"
            elif event.key == pygame.K_2:
                mode = "rectangle"
            elif event.key == pygame.K_3:
                mode = "circle"
            elif event.key == pygame.K_4:
                mode = "eraser"
            elif event.key == pygame.K_5:
                mode = "square"
            elif event.key == pygame.K_6:
                mode = "right_triangle"
            elif event.key == pygame.K_7:
                mode = "equilateral_triangle"
            elif event.key == pygame.K_8:
                mode = "rhombus"

            # Size
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

            x1, y1 = start_pos
            x2, y2 = end_pos

            # Rectangle
            if mode == "rectangle":
                rect = pygame.Rect(min(x1, x2), min(y1, y2),
                                   abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, color, rect, 3)

            # Circle
            elif mode == "circle":
                r = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, r, 3)

            # Square
            elif mode == "square":
                side = min(abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, color, (x1, y1, side, side), 3)

            # Right triangle
            elif mode == "right_triangle":
                points = [(x1, y1), (x1, y2), (x2, y2)]
                pygame.draw.polygon(screen, color, points, 3)

            # Equilateral triangle
            elif mode == "equilateral_triangle":
                side = abs(x2 - x1)
                h = int(side * math.sqrt(3) / 2)
                points = [(x1, y1), (x1 + side, y1), (x1 + side // 2, y1 - h)]
                pygame.draw.polygon(screen, color, points, 3)

            # Rhombus
            elif mode == "rhombus":
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                pygame.draw.polygon(screen, color, points, 3)

        # Drawing (brush / eraser)
        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "brush":
                pygame.draw.circle(screen, color, event.pos, radius)
            elif mode == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, radius)

    # Рисуем инструкцию КАЖДЫЙ кадр
    draw_instructions()

    pygame.display.update()
    clock.tick(60)