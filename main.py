import pygame
import sys
import time
import random
import os
from game import Game
from colors import Colors

pygame.init()
pygame.mixer.init()

base_path = os.path.dirname(os.path.abspath(__file__))
sounds_path = os.path.join(base_path, 'sounds')

songs = [
    os.path.join(sounds_path, 'song1.mp3'),
    os.path.join(sounds_path, 'song2.mp3'),
    os.path.join(sounds_path, 'song3.mp3'),
]

def play_random_song():
    song = random.choice(songs)
    print("Playing:", song) 
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.5)

play_random_song()

MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

# Fonty a texty
title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("Game Over", True, Colors.white)

# UI obdélníky
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

# Okno a herní hodiny
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# Herní objekt
game = Game()

# Událost pro pád bloku
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

# Časovače pro podržení kláves
move_delay = 0.1  # sekundy mezi pohyby
last_move_time = time.time()

# Herní smyčka
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.game_over:
                game.game_over = False
                game.reset()

            if not game.game_over:
                if event.key == pygame.K_UP:
                    game.rotate()

        if event.type == GAME_UPDATE and not game.game_over:
            game.move_down()

    # Podržené klávesy
    keys = pygame.key.get_pressed()
    current_time = time.time()

    if not game.game_over and current_time - last_move_time > move_delay:
        if keys[pygame.K_LEFT]:
            game.move_left()
            last_move_time = current_time
        elif keys[pygame.K_RIGHT]:
            game.move_right()
            last_move_time = current_time
        elif keys[pygame.K_DOWN]:
            game.move_down()
            game.update_score(0, 1)
            last_move_time = current_time

    # Kreslení UI
    score_value_surface = title_font.render(str(game.score), True, Colors.white)

    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20))
    screen.blit(next_surface, (375, 180))

    if game.game_over:
        screen.blit(game_over_surface, (320, 450))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))

    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)

    game.draw(screen)

    pygame.display.update()

    clock.tick(60)
