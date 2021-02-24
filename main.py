import pygame
import pygame.freetype
import random
import time
import mover

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

def clear(window):
    window.fill((255, 255, 255))

def update(x, y, plus_x, plus_y):
    return (x+plus_x, y+plus_y)

def trim(v, upper, lower):
    if v > upper:
        return upper
    if v < lower:
        return lower
    return v

def handle_bounds(x, y, x_bound, y_bound):
    return trim(x, x_bound, 0), trim(y, y_bound, 0)


def make_color(ind):
    if ind == 0:
        return 255, 0, 0
    if ind == 1:
        return 0, 255, 0
    return 0, 0, 255

def update_player(player_color, player_coords, player_velocity, scr_h, scr_w):
    new_y = player_coords[0] + player_velocity[0]
    new_x = player_coords[1] + player_velocity[1]
    new_velocity_y = player_velocity[0] + random.randint(-2, 2)
    new_velocity_x = player_velocity[1] + random.randint(-2, 2)
    new_y, new_x = handle_bounds(new_x, new_y, scr_w, scr_h)
    return player_color, (new_y, new_x), (trim(new_velocity_y, 5, -5), trim(new_velocity_x, 5, -5))

# Set up the drawing window

move_speed = 5
screen_height = 1000
screen_width = 750
screen_size = (screen_width, screen_height + screen_height // 10)
quarter_height = screen_height//4
quarter_width = screen_width//4
coords = (quarter_height * 2, quarter_width * 2)
frames_per_second = 50
player_count = 3
max_velo = 5
max_accel = 2
radius = 15

font = pygame.font.Font(pygame.font.get_default_font(), 18)

rock = pygame.image.load("rock.png")
scissors = pygame.image.load("scissors.png")
paper = pygame.image.load("paper.png")
rock = pygame.transform.scale(rock, (radius*2, radius*2))
paper = pygame.transform.scale(paper, (radius*2, radius*2))
scissors = pygame.transform.scale(scissors, (radius*2, radius*2))

choices = [rock, scissors, paper]


screen = pygame.display.set_mode([screen_height, screen_width])

wins = [0, 0, 0]
going = True
while going:
    players = []
    for t in [0, 1, 2]:
        for _ in range(player_count):
            coords = (
            random.randint(quarter_height, 3 * quarter_height), random.randint(quarter_width, quarter_width * 3))
            velocity = (random.randint(-max_velo, max_velo), random.randint(-max_velo, max_velo))
            accel = (random.randint(-max_accel, max_accel), random.randint(-max_accel, max_accel))
            players.append(mover.Mover(t, coords, velocity, accel, screen_width, screen_height, max_velo, max_accel))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            if event.type == KEYDOWN and event.key == K_UP:
                print("")
                for player in players:
                    print(player)
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == KEYDOWN and event.key == K_DOWN:
                            waiting = False

        visited = []
        positions = []
        totals = [0, 0, 0]
        for player in players:
            player.update_position()

        for player in players:
            for index in range(len(positions)):
                distance = (positions[index][0] - player.get_position()[0]) ** 2 + (positions[index][1] - player.get_position()[1]) ** 2
                if distance < (radius*2) ** 2:
                    visited[index].update_color(player.get_color())
                    player.update_color(visited[index].get_color())
            visited.append(player)
            positions.append(player.get_position())
            totals[player.get_color()] += 1

        for i in [0, 1, 2]:
            if totals[i] == player_count*3:
                wins[i] += 1
                running = False
        players = visited

        for player in players:
            screen.blit(choices[player.get_color()], player.get_position())

        pygame.display.flip()

        time.sleep(1/frames_per_second)
        clear(screen)

    screen.blit(font.render('Game Over! Current Records:', True, (0, 0, 0)), dest=(screen_width//10,4*screen_height//10))
    screen.blit(font.render('Rock: ' + str(wins[0]) + ' Paper: ' + str(wins[2]) + ' Scissors: ' + str(wins[1]), True, (0, 0, 0)), dest=(screen_width//10,5*screen_height//10))
    screen.blit(font.render('Press Escape to Exit, Press any other key to go again', True, (0, 0, 0)), dest=(screen_width//10,6*screen_height//10))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN:
                waiting = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False

pygame.quit()