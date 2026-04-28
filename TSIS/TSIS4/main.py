import pygame
import sys
import db
from game import run_game

pygame.init()
screen = pygame.display.set_mode((400,600))
font = pygame.font.SysFont("Verdana", 20)

def get_username():
    username=""
    while True:
        screen.fill((255,255,255))
        text=font.render("Enter name: "+username,True,(0,0,0))
        screen.blit(text,(50,250))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    return username
                elif event.key==pygame.K_BACKSPACE:
                    username=username[:-1]
                else:
                    username+=event.unicode

def show_leaderboard():
    data = db.get_top10()
    while True:
        screen.fill((255,255,255))

        for i,row in enumerate(data):
            text=font.render(f"{i+1}. {row[0]} {row[1]}",True,(0,0,0))
            screen.blit(text,(50,50+i*30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                return

def menu():
    while True:
        screen.fill((255,255,255))
        screen.blit(font.render("1 Play",True,(0,0,0)),(150,200))
        screen.blit(font.render("2 Leaderboard",True,(0,0,0)),(150,250))
        screen.blit(font.render("ESC Quit",True,(0,0,0)),(150,300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    username=get_username()
                    player_id=db.get_or_create_player(username)
                    run_game(player_id, db)
                if event.key==pygame.K_2:
                    show_leaderboard()
                if event.key==pygame.K_ESCAPE:
                    sys.exit()

menu()