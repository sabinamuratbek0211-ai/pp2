import pygame
import random
import sys

pygame.init()

# Screen settings
WIDTH = 400
HEIGHT = 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Snake settings
snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"
next_direction = "RIGHT"

score = 0
level = 1
speed = 7


def generate_food():
    # Generate food not on snake
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        if (x, y) not in snake:
            return (x, y)


food = generate_food()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Control snake direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                next_direction = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                next_direction = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                next_direction = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                next_direction = "RIGHT"

    direction = next_direction

    head_x, head_y = snake[0]

    # Move snake head
    if direction == "UP":
        head_y -= CELL
    elif direction == "DOWN":
        head_y += CELL
    elif direction == "LEFT":
        head_x -= CELL
    elif direction == "RIGHT":
        head_x += CELL

    new_head = (head_x, head_y)

    # Check wall collision
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        pygame.quit()
        sys.exit()

    # Check collision with itself
    if new_head in snake:
        pygame.quit()
        sys.exit()

    snake.insert(0, new_head)

    # Check food collision
    if new_head == food:
        score += 1

        # Add level every 4 foods
        if score % 4 == 0:
            level += 1
            speed += 2

        food = generate_food()
    else:
        snake.pop()

    # Draw background
    screen.fill(WHITE)

    # Draw snake
    for block in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], CELL, CELL))

    # Draw food
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL, CELL))

    # Show score and level
    text = font.render(f"Score: {score}  Level: {level}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(speed)