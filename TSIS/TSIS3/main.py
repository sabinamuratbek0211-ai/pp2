import pygame
import sys

from persistence import load_settings
from ui import main_menu, username_screen, leaderboard_screen, settings_screen, game_over_screen
from racer import game_loop

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Racer")

clock = pygame.time.Clock()

settings = load_settings()

while True:
    action = main_menu(screen, clock)

    if action == "quit":
        pygame.quit()
        sys.exit()

    elif action == "play":
        username = username_screen(screen, clock)

        if username is None:
            pygame.quit()
            sys.exit()

        result, score, distance, coins = game_loop(screen, clock, settings, username)

        while result == "game_over":
            next_action = game_over_screen(screen, clock, score, distance, coins)

            if next_action == "retry":
                result, score, distance, coins = game_loop(screen, clock, settings, username)

            elif next_action == "menu":
                break

            elif next_action == "quit":
                pygame.quit()
                sys.exit()

    elif action == "leaderboard":
        result = leaderboard_screen(screen, clock)

        if result == "quit":
            pygame.quit()
            sys.exit()

    elif action == "settings":
        result = settings_screen(screen, clock, settings)

        if result == "quit":
            pygame.quit()
            sys.exit()