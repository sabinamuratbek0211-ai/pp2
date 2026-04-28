import pygame
from persistence import load_leaderboard, save_settings

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (70, 130, 255)
GREEN = (0, 180, 0)
RED = (220, 50, 50)


class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen, font):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text = font.render(self.text, True, BLACK)
        screen.blit(
            text,
            (
                self.rect.centerx - text.get_width() // 2,
                self.rect.centery - text.get_height() // 2
            )
        )

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


def username_screen(screen, clock):
    font = pygame.font.SysFont("Verdana", 24)
    name = ""

    while True:
        screen.fill(WHITE)

        title = font.render("Enter your name:", True, BLACK)
        screen.blit(title, (70, 180))

        box = pygame.Rect(70, 230, 260, 45)
        pygame.draw.rect(screen, WHITE, box)
        pygame.draw.rect(screen, BLACK, box, 2)

        name_text = font.render(name, True, BLACK)
        screen.blit(name_text, (80, 238))

        hint = font.render("Press ENTER to start", True, BLACK)
        screen.blit(hint, (55, 310))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip() != "":
                    return name.strip()

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 12:
                        name += event.unicode

        pygame.display.update()
        clock.tick(60)


def main_menu(screen, clock):
    font = pygame.font.SysFont("Verdana", 24)

    buttons = {
        "play": Button("Play", 100, 180, 200, 50),
        "leaderboard": Button("Leaderboard", 100, 250, 200, 50),
        "settings": Button("Settings", 100, 320, 200, 50),
        "quit": Button("Quit", 100, 390, 200, 50)
    }

    while True:
        screen.fill(WHITE)

        title = font.render("RACER GAME", True, BLACK)
        screen.blit(title, (105, 90))

        for button in buttons.values():
            button.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for key, button in buttons.items():
                    if button.clicked(pos):
                        return key

        pygame.display.update()
        clock.tick(60)


def leaderboard_screen(screen, clock):
    font = pygame.font.SysFont("Verdana", 20)
    small_font = pygame.font.SysFont("Verdana", 16)

    back = Button("Back", 120, 520, 160, 45)

    while True:
        screen.fill(WHITE)

        title = font.render("TOP 10 SCORES", True, BLACK)
        screen.blit(title, (105, 40))

        data = load_leaderboard()

        y = 100
        for i, item in enumerate(data):
            text = small_font.render(
                f"{i + 1}. {item['name']} | Score: {item['score']} | Dist: {item['distance']}m",
                True,
                BLACK
            )
            screen.blit(text, (20, y))
            y += 35

        back.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.clicked(pygame.mouse.get_pos()):
                    return "menu"

        pygame.display.update()
        clock.tick(60)


def settings_screen(screen, clock, settings):
    font = pygame.font.SysFont("Verdana", 20)

    sound_button = Button("Sound: ON" if settings["sound"] else "Sound: OFF", 80, 150, 240, 45)
    color_button = Button("Car color: " + settings["car_color"], 80, 220, 240, 45)
    difficulty_button = Button("Difficulty: " + settings["difficulty"], 80, 290, 240, 45)
    back = Button("Back", 120, 500, 160, 45)

    colors = ["blue", "red", "green"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(WHITE)

        title = font.render("SETTINGS", True, BLACK)
        screen.blit(title, (140, 70))

        sound_button.text = "Sound: ON" if settings["sound"] else "Sound: OFF"
        color_button.text = "Car color: " + settings["car_color"]
        difficulty_button.text = "Difficulty: " + settings["difficulty"]

        sound_button.draw(screen, font)
        color_button.draw(screen, font)
        difficulty_button.draw(screen, font)
        back.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if sound_button.clicked(pos):
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                elif color_button.clicked(pos):
                    index = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(index + 1) % len(colors)]
                    save_settings(settings)

                elif difficulty_button.clicked(pos):
                    index = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                    save_settings(settings)

                elif back.clicked(pos):
                    return "menu"

        pygame.display.update()
        clock.tick(60)


def game_over_screen(screen, clock, score, distance, coins):
    font = pygame.font.SysFont("Verdana", 22)

    retry = Button("Retry", 100, 360, 200, 50)
    menu = Button("Main Menu", 100, 430, 200, 50)

    while True:
        screen.fill(WHITE)

        title = font.render("GAME OVER", True, RED)
        screen.blit(title, (125, 100))

        screen.blit(font.render("Score: " + str(score), True, BLACK), (110, 180))
        screen.blit(font.render("Distance: " + str(distance) + "m", True, BLACK), (110, 220))
        screen.blit(font.render("Coins: " + str(coins), True, BLACK), (110, 260))

        retry.draw(screen, font)
        menu.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if retry.clicked(pos):
                    return "retry"

                if menu.clicked(pos):
                    return "menu"

        pygame.display.update()
        clock.tick(60)