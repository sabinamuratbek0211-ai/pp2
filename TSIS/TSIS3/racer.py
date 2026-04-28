import pygame
import random
from pygame.locals import *
from persistence import add_score

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROAD = (60, 60, 60)
YELLOW = (255, 220, 0)

LANES = [80, 160, 240, 320]
FINISH_DISTANCE = 3000


def load_image(path, size):
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, size)
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = load_image("assets/Player.png", (50, 85))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 500)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_LEFT] and self.rect.left > 30:
            self.rect.move_ip(-5, 0)

        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH - 30:
            self.rect.move_ip(5, 0)


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, speed, player_rect):
        super().__init__()

        self.image = load_image("assets/Enemy.png", (50, 85))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset_position(player_rect)

    def reset_position(self, player_rect):
        while True:
            self.rect.center = (
                random.choice(LANES),
                random.randint(-700, -120)
            )

            if abs(self.rect.centerx - player_rect.centerx) > 40:
                break

    def move(self, player_rect):
        self.rect.y += self.speed

        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position(player_rect)


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.speed = speed
        self.weight = 1
        self.image = None
        self.rect = None
        self.reset_position()

    def reset_position(self):
        self.weight = random.choice([1, 2, 3])

        if self.weight == 1:
            size = 28
        elif self.weight == 2:
            size = 34
        else:
            size = 40

        self.image = load_image("assets/Coin.png", (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.choice(LANES),
            random.randint(-500, -80)
        )

    def move(self):
        self.rect.y += self.speed

        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed, player_rect):
        super().__init__()

        self.speed = speed
        self.kind = None
        self.image = None
        self.rect = None
        self.reset_position(player_rect)

    def set_image(self):
        if self.kind == "barrier":
            self.image = load_image("assets/barrier.png", (60, 40))

        elif self.kind == "oil":
            self.image = load_image("assets/oil.png", (60, 35))

        elif self.kind == "pothole":
            self.image = load_image("assets/pothole.png", (60, 35))

    def reset_position(self, player_rect):
        self.kind = random.choice(["barrier", "oil", "pothole"])
        self.set_image()

        self.rect = self.image.get_rect()

        while True:
            self.rect.center = (
                random.choice(LANES),
                random.randint(-800, -150)
            )

            if abs(self.rect.centerx - player_rect.centerx) > 40:
                break

    def move(self, player_rect):
        self.rect.y += self.speed

        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position(player_rect)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.speed = speed
        self.kind = None
        self.image = None
        self.rect = None
        self.spawn_time = pygame.time.get_ticks()
        self.timeout = 6000

        self.reset_position()

    def set_image(self):
        if self.kind == "Nitro":
            self.image = load_image("assets/nitro.png", (50, 50))

        elif self.kind == "Shield":
            self.image = load_image("assets/shield.png", (50, 50))

        elif self.kind == "Repair":
            self.image = load_image("assets/repair.png", (50, 50))

    def reset_position(self):
        self.kind = random.choice(["Nitro", "Shield", "Repair"])
        self.set_image()

        self.rect = self.image.get_rect()
        self.rect.center = (
            random.choice(LANES),
            random.randint(-1000, -250)
        )

        self.spawn_time = pygame.time.get_ticks()

    def move(self):
        self.rect.y += self.speed

        now = pygame.time.get_ticks()

        if self.rect.top > SCREEN_HEIGHT or now - self.spawn_time > self.timeout:
            self.reset_position()


def get_difficulty(settings):
    if settings["difficulty"] == "easy":
        return 3, 2, 2
    elif settings["difficulty"] == "hard":
        return 6, 4, 4
    return 4, 3, 3


def draw_road(screen, road_offset):
    screen.fill(WHITE)

    pygame.draw.rect(screen, ROAD, (30, 0, 340, SCREEN_HEIGHT))

    for x in [120, 200, 280]:
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT), 2)

    for y in range(-40, SCREEN_HEIGHT, 80):
        pygame.draw.rect(screen, YELLOW, (195, y + road_offset, 10, 40))


def game_loop(screen, clock, settings, username):
    font = pygame.font.SysFont("Verdana", 18)

    base_speed, traffic_count, obstacle_count = get_difficulty(settings)

    player = Player()

    traffic = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    for _ in range(traffic_count):
        traffic.add(TrafficCar(base_speed, player.rect))

    for _ in range(obstacle_count):
        obstacles.add(Obstacle(base_speed, player.rect))

    for _ in range(3):
        coins.add(Coin(base_speed))

    powerups.add(PowerUp(base_speed))

    coins_collected = 0
    distance = 0
    score = 0

    active_power = None
    power_start = 0
    power_duration = 0

    road_offset = 0
    running = True

    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score, distance, coins_collected

        player.move()

        current_speed = base_speed

        if active_power == "Nitro":
            current_speed += 4

            if now - power_start > power_duration:
                active_power = None

        distance += current_speed // 2
        road_offset = (road_offset + current_speed) % 80

        if distance > 1000:
            current_speed += 1

        if distance > 2000:
            current_speed += 2

        for car in traffic:
            car.speed = current_speed
            car.move(player.rect)

        for obstacle in obstacles:
            obstacle.speed = current_speed
            obstacle.move(player.rect)

        for coin in coins:
            coin.speed = current_speed
            coin.move()

        for powerup in powerups:
            powerup.speed = current_speed
            powerup.move()

        for coin in pygame.sprite.spritecollide(player, coins, False):
            coins_collected += coin.weight
            coin.reset_position()

        for powerup in pygame.sprite.spritecollide(player, powerups, False):
            if active_power is None:
                active_power = powerup.kind
                power_start = now

                if active_power == "Nitro":
                    power_duration = 4000

                elif active_power == "Shield":
                    power_duration = 0

                elif active_power == "Repair":
                    if len(obstacles) > 0:
                        random.choice(obstacles.sprites()).reset_position(player.rect)
                    active_power = None

            powerup.reset_position()

        if pygame.sprite.spritecollide(player, traffic, False):
            if active_power == "Shield":
                active_power = None

                for car in traffic:
                    if player.rect.colliderect(car.rect):
                        car.reset_position(player.rect)
            else:
                running = False

        for obstacle in pygame.sprite.spritecollide(player, obstacles, False):
            if active_power == "Shield":
                active_power = None
                obstacle.reset_position(player.rect)

            else:
                if obstacle.kind == "oil":
                    player.rect.x += random.choice([-40, 40])

                    if player.rect.left < 30:
                        player.rect.left = 30

                    if player.rect.right > SCREEN_WIDTH - 30:
                        player.rect.right = SCREEN_WIDTH - 30

                elif obstacle.kind == "pothole":
                    distance = max(0, distance - 50)

                elif obstacle.kind == "barrier":
                    running = False

                obstacle.reset_position(player.rect)

        score = coins_collected * 10 + distance

        if active_power == "Nitro":
            score += 50

        if distance >= FINISH_DISTANCE:
            running = False

        draw_road(screen, road_offset)

        traffic.draw(screen)
        obstacles.draw(screen)
        coins.draw(screen)
        powerups.draw(screen)
        screen.blit(player.image, player.rect)

        remaining = max(0, FINISH_DISTANCE - distance)

        screen.blit(font.render("Coins: " + str(coins_collected), True, BLACK), (10, 10))
        screen.blit(font.render("Score: " + str(score), True, BLACK), (10, 35))
        screen.blit(font.render("Distance: " + str(distance) + "m", True, BLACK), (10, 60))
        screen.blit(font.render("Left: " + str(remaining) + "m", True, BLACK), (10, 85))

        if active_power is None:
            power_text = "Power: None"

        elif active_power == "Nitro":
            left = max(0, (power_duration - (now - power_start)) // 1000)
            power_text = "Power: Nitro " + str(left) + "s"

        else:
            power_text = "Power: Shield"

        screen.blit(font.render(power_text, True, BLACK), (10, 110))

        pygame.display.update()
        clock.tick(60)

    add_score(username, score, distance)

    return "game_over", score, distance, coins_collected