import pygame
import sys
import random
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

font = pygame.font.SysFont("Verdana", 20)

coins_collected = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load enemy image
        self.image = pygame.image.load("Enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 90))

        # Get rectangle around enemy image
        self.rect = self.image.get_rect()

        # Start enemy above the screen at random x-position
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -90)

    def move(self):
        # Move enemy down
        self.rect.move_ip(0, 4)

        # If enemy goes below the screen, move it back to the top
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -90)

    def draw(self, surface):
        # Draw enemy on the screen
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Player.png").convert_alpha()
        self.image = self.image.subsurface(self.image.get_bounding_rect()).copy()
        self.image = pygame.transform.scale(self.image, (120, 110))

        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-4, 0)

        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(4, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load coin image
        self.image = pygame.image.load("Coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))

        # Get rectangle around coin image
        self.rect = self.image.get_rect()

        # Start coin above the screen
        self.reset_position()

    def move(self):
        # Move coin down
        self.rect.move_ip(0, 3)

        # If coin goes below the screen, reset its position
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

    def reset_position(self):
        # Put coin at random x-position above the screen
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-300, -50)
        )

    def draw(self, surface):
        # Draw coin on the screen
        surface.blit(self.image, self.rect)


# Create objects
P1 = Player()
E1 = Enemy()
C1 = Coin()


# Main game loop
while True:

    # Check events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update object positions
    P1.update()
    E1.move()
    C1.move()

    # Smaller hitboxes for better collision
    player_hitbox = P1.rect.inflate(-30, -30)
    enemy_hitbox = E1.rect.inflate(-30, -30)

    # Check collision with enemy
    if player_hitbox.colliderect(enemy_hitbox):
        pygame.quit()
        sys.exit()

    # Check collision with coin
    if pygame.sprite.collide_rect(P1, C1):
        coins_collected += 1
        C1.reset_position()

    # Fill background
    DISPLAYSURF.fill(WHITE)

    # Draw objects
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
    C1.draw(DISPLAYSURF)

    # Draw coins counter
    coins_text = font.render("Coins: " + str(coins_collected), True, BLACK)
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 120, 10))

    # Update display
    pygame.display.update()

    # Set FPS
    FramePerSec.tick(FPS)