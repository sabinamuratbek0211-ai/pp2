import pygame
import sys
import random
from pygame.locals import *

pygame.init()

FPS = 60
clock = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

font = pygame.font.SysFont("Verdana", 20)

coins_collected = 0
enemy_speed = 4
speed_increase_every = 5


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load and scale player image
        self.image = pygame.image.load("Player.png").convert_alpha()
        self.image = self.image.subsurface(self.image.get_bounding_rect()).copy()
        self.image = pygame.transform.scale(self.image, (80, 110))

        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 520)

    def move(self):
        # Move player left and right
        keys = pygame.key.get_pressed()

        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load and scale enemy image
        self.image = pygame.image.load("Enemy.png").convert_alpha()
        self.image = self.image.subsurface(self.image.get_bounding_rect()).copy()
        self.image = pygame.transform.scale(self.image, (50, 90))

        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        # Put enemy above the screen at random x position
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -90)

    def move(self):
        # Move enemy down
        self.rect.move_ip(0, enemy_speed)

        # Reset enemy when it leaves the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.weight = 1
        self.image = None
        self.rect = None
        self.reset_position()

    def reset_position(self):
        # Random coin weight
        self.weight = random.choice([1, 2, 3])

        # Different size depending on coin weight
        if self.weight == 1:
            size = 25
        elif self.weight == 2:
            size = 32
        else:
            size = 40

        # Load coin image
        self.image = pygame.image.load("Coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))

        self.rect = self.image.get_rect()

        # Put coin above the road
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-300, -50)
        )

    def move(self):
        # Move coin down
        self.rect.move_ip(0, 3)

        # Reset coin when it leaves the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()


player = Player()
enemy = Enemy()
coin = Coin()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    player.move()
    enemy.move()
    coin.move()

    # Check collision with enemy
    if player.rect.colliderect(enemy.rect):
        pygame.quit()
        sys.exit()

    # Check collision with coin
    if player.rect.colliderect(coin.rect):
        coins_collected += coin.weight
        coin.reset_position()

        # Increase enemy speed every N coins
        enemy_speed = 4 + coins_collected // speed_increase_every

    screen.fill(WHITE)

    screen.blit(player.image, player.rect)
    screen.blit(enemy.image, enemy.rect)
    screen.blit(coin.image, coin.rect)

    coins_text = font.render("Coins: " + str(coins_collected), True, BLACK)
    speed_text = font.render("Speed: " + str(enemy_speed), True, BLACK)

    screen.blit(coins_text, (10, 10))
    screen.blit(speed_text, (10, 40))

    pygame.display.update()
    clock.tick(FPS)
    