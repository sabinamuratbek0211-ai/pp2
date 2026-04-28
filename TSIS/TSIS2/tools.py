import pygame
import math
from collections import deque


def flood_fill(surface, start, fill_color):
    width, height = surface.get_size()
    x, y = start

    target_color = surface.get_at((x, y))

    if target_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        x, y = queue.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), fill_color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))


def draw_shape(surface, mode, start, end, color, size):
    x1, y1 = start
    x2, y2 = end

    if mode == "line":
        pygame.draw.line(surface, color, start, end, size)

    elif mode == "rectangle":
        rect = pygame.Rect(
            min(x1, x2),
            min(y1, y2),
            abs(x2 - x1),
            abs(y2 - y1)
        )
        pygame.draw.rect(surface, color, rect, size)

    elif mode == "circle":
        radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        pygame.draw.circle(surface, color, start, radius, size)

    elif mode == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))

        if x2 < x1:
            side_x = -side
        else:
            side_x = side

        if y2 < y1:
            side_y = -side
        else:
            side_y = side

        pygame.draw.rect(surface, color, (x1, y1, side_x, side_y), size)

    elif mode == "right_triangle":
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, size)

    elif mode == "equilateral_triangle":
        side = abs(x2 - x1)
        height = int(side * math.sqrt(3) / 2)

        if x2 >= x1:
            left = x1
        else:
            left = x1 - side

        if y2 >= y1:
            points = [
                (left, y1),
                (left + side, y1),
                (left + side // 2, y1 + height)
            ]
        else:
            points = [
                (left, y1),
                (left + side, y1),
                (left + side // 2, y1 - height)
            ]

        pygame.draw.polygon(surface, color, points, size)

    elif mode == "rhombus":
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        points = [
            (center_x, y1),
            (x2, center_y),
            (center_x, y2),
            (x1, center_y)
        ]

        pygame.draw.polygon(surface, color, points, size)