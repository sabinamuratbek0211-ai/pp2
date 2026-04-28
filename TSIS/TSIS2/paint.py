import pygame
import sys
from datetime import datetime
from tools import flood_fill, draw_shape

pygame.init()

WIDTH = 640
HEIGHT = 480
TOOLBAR_WIDTH = 180
CANVAS_WIDTH = WIDTH - TOOLBAR_WIDTH

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 14)
text_font = pygame.font.SysFont("Verdana", 22)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)

canvas = pygame.Surface((CANVAS_WIDTH, HEIGHT))
canvas.fill(WHITE)

color = BLUE
mode = "pencil"
brush_size = 5

drawing = False
start_pos = None
last_pos = None

typing = False
text_pos = None
current_text = ""


def is_on_canvas(pos):
    return pos[0] < CANVAS_WIDTH


def save_canvas():
    filename = "paint_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
    pygame.image.save(canvas, filename)
    print("Saved:", filename)


def draw_toolbar():
    pygame.draw.rect(screen, (230, 230, 230), (CANVAS_WIDTH, 0, TOOLBAR_WIDTH, HEIGHT))

    instructions = [
        "TOOLS:",
        "P - Pencil",
        "L - Line",
        "R - Rectangle",
        "C - Circle",
        "E - Eraser",
        "S - Square",
        "A - Right triangle",
        "Q - Equilateral",
        "D - Rhombus",
        "F - Fill",
        "T - Text",
        "",
        "COLORS:",
        "O - Red",
        "G - Green",
        "B - Blue",
        "K - Black",
        "",
        "SIZE:",
        "1 - Small",
        "2 - Medium",
        "3 - Large",
        "",
        "Ctrl + S - Save",
        "Enter - confirm text",
        "Esc - cancel text",
        "",
        "Current:",
        "Tool: " + mode,
        "Size: " + str(brush_size)
    ]

    y = 10
    for line in instructions:
        text = font.render(line, True, BLACK)
        screen.blit(text, (CANVAS_WIDTH + 10, y))
        y += 17

    pygame.draw.rect(screen, color, (CANVAS_WIDTH + 10, HEIGHT - 35, 40, 25))
    pygame.draw.rect(screen, BLACK, (CANVAS_WIDTH + 10, HEIGHT - 35, 40, 25), 2)


while True:
    preview_canvas = canvas.copy()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if typing:
                if event.key == pygame.K_RETURN:
                    rendered_text = text_font.render(current_text, True, color)
                    canvas.blit(rendered_text, text_pos)

                    typing = False
                    current_text = ""

                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    current_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    current_text = current_text[:-1]

                else:
                    current_text += event.unicode

            else:
                keys = pygame.key.get_pressed()

                if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and event.key == pygame.K_s:
                    save_canvas()

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_p:
                    mode = "pencil"

                elif event.key == pygame.K_l:
                    mode = "line"

                elif event.key == pygame.K_r:
                    mode = "rectangle"

                elif event.key == pygame.K_c:
                    mode = "circle"

                elif event.key == pygame.K_e:
                    mode = "eraser"

                elif event.key == pygame.K_s:
                    mode = "square"

                elif event.key == pygame.K_a:
                    mode = "right_triangle"

                elif event.key == pygame.K_q:
                    mode = "equilateral_triangle"

                elif event.key == pygame.K_d:
                    mode = "rhombus"

                elif event.key == pygame.K_f:
                    mode = "fill"

                elif event.key == pygame.K_t:
                    mode = "text"

                elif event.key == pygame.K_o:
                    color = RED

                elif event.key == pygame.K_g:
                    color = GREEN

                elif event.key == pygame.K_b:
                    color = BLUE

                elif event.key == pygame.K_k:
                    color = BLACK

                elif event.key == pygame.K_1:
                    brush_size = 2

                elif event.key == pygame.K_2:
                    brush_size = 5

                elif event.key == pygame.K_3:
                    brush_size = 10

        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_on_canvas(event.pos):

                if mode == "fill":
                    flood_fill(canvas, event.pos, color)

                elif mode == "text":
                    typing = True
                    text_pos = event.pos
                    current_text = ""

                else:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

        if event.type == pygame.MOUSEMOTION and drawing:
            if is_on_canvas(event.pos):

                if mode == "pencil":
                    pygame.draw.line(canvas, color, last_pos, event.pos, brush_size)
                    last_pos = event.pos

                elif mode == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, event.pos, brush_size)
                    last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                drawing = False

                if is_on_canvas(event.pos):
                    end_pos = event.pos

                    if mode not in ["pencil", "eraser"]:
                        draw_shape(canvas, mode, start_pos, end_pos, color, brush_size)

    if drawing and start_pos is not None:
        mouse_pos = pygame.mouse.get_pos()

        if is_on_canvas(mouse_pos):
            if mode not in ["pencil", "eraser"]:
                preview_canvas = canvas.copy()
                draw_shape(preview_canvas, mode, start_pos, mouse_pos, color, brush_size)

    screen.fill(WHITE)
    screen.blit(preview_canvas, (0, 0))

    if typing and text_pos is not None:
        text_preview = text_font.render(current_text + "|", True, color)
        screen.blit(text_preview, text_pos)

    draw_toolbar()

    pygame.display.update()
    clock.tick(60)