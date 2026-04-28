import pygame
import random
import sys

pygame.init()

# Screen
WIDTH = 400
HEIGHT = 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,180,0)
RED = (0,200,0)        # обычная еда (зелёная — логично)
POISON_COLOR = (200,0,0)  # яд — ярко красный
GRAY = (200,200,200)

# Snake
snake = [(100,100),(80,100),(60,100)]
direction = "RIGHT"
next_dir = "RIGHT"

score = 0
level = 1
speed = 7

# Таймеры
FOOD_LIFETIME = 5000
POISON_LIFETIME = 6000

def rand_pos():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x,y) not in snake:
            return (x,y)

# Food
food = {
    "pos": rand_pos(),
    "time": pygame.time.get_ticks()
}

# Poison
poison = {
    "pos": rand_pos(),
    "time": pygame.time.get_ticks()
}

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                next_dir = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                next_dir = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                next_dir = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                next_dir = "RIGHT"

    direction = next_dir

    # движение
    x,y = snake[0]

    if direction=="UP": y-=CELL
    if direction=="DOWN": y+=CELL
    if direction=="LEFT": x-=CELL
    if direction=="RIGHT": x+=CELL

    head = (x,y)

    # столкновения
    if x<0 or y<0 or x>=WIDTH or y>=HEIGHT:
        break

    if head in snake:
        break

    snake.insert(0, head)

    # еда
    if head == food["pos"]:
        score += 1

        food = {
            "pos": rand_pos(),
            "time": pygame.time.get_ticks()
        }

        if score % 4 == 0:
            level += 1
            speed += 1

    else:
        snake.pop()

    # яд
    if head == poison["pos"]:
        for _ in range(2):
            if len(snake) > 1:
                snake.pop()

        if len(snake) <= 1:
            break

        poison = {
            "pos": rand_pos(),
            "time": pygame.time.get_ticks()
        }

    now = pygame.time.get_ticks()

    # исчезновение еды
    if now - food["time"] > FOOD_LIFETIME:
        food = {
            "pos": rand_pos(),
            "time": now
        }

    # исчезновение яда (ВАЖНО)
    if now - poison["time"] > POISON_LIFETIME:
        poison = {
            "pos": rand_pos(),
            "time": now
        }

    # рисуем
    screen.fill(WHITE)

    # GRID (если хочешь можно убрать)
    for xg in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (xg,0),(xg,HEIGHT))
    for yg in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0,yg),(WIDTH,yg))

    # snake
    for s in snake:
        pygame.draw.rect(screen, GREEN, (*s, CELL, CELL))

    # обычная еда (зелёная)
    pygame.draw.rect(screen, RED, (*food["pos"], CELL, CELL))

    # ЯД (красный + крест)
    pygame.draw.rect(screen, POISON_COLOR, (*poison["pos"], CELL, CELL))

    pygame.draw.line(screen, WHITE,
                     poison["pos"],
                     (poison["pos"][0]+CELL, poison["pos"][1]+CELL), 2)

    pygame.draw.line(screen, WHITE,
                     (poison["pos"][0]+CELL, poison["pos"][1]),
                     (poison["pos"][0], poison["pos"][1]+CELL), 2)

    # UI
    text = font.render(f"Score:{score} Level:{level}", True, BLACK)
    screen.blit(text,(10,10))

    pygame.display.flip()
    clock.tick(speed)