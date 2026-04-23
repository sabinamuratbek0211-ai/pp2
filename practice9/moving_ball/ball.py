import pygame


class Ball:
    def __init__(self, x, y, radius=25, color=(255, 0, 0), step=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.step = step

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move_up(self):
        if self.y - self.step - self.radius >= 0:
            self.y -= self.step

    def move_down(self, height):
        if self.y + self.step + self.radius <= height:
            self.y += self.step

    def move_left(self):
        if self.x - self.step - self.radius >= 0:
            self.x -= self.step

    def move_right(self, width):
        if self.x + self.step + self.radius <= width:
            self.x += self.step