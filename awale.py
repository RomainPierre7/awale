import pygame
import math
import time
import random

# Pygame Initialization
font_sys = "impact"
pygame.init()
screen = pygame.display.set_mode((0, 0))
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("Awale")
screen.fill((150, 70, 30))
pygame.display.update()

# Board initialization
board = [[4 for _ in range(6)] for _ in range(2)]
attic = [0, 0]
radius = width // 20
board_loc = [[(width // 2 + (j - 2.5) * radius * 2.5, height // 2 + (i - 0.5) * radius * 2.5) for j in range(6)] for i in range(2)]
rotation = [[0, 5], [0, 4], [0, 3], [0, 2], [0, 1], [0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5]]

# Functions
def update_screen(player, turn):
    screen.fill((150, 70, 30))
    font = pygame.font.SysFont(font_sys, 100)
    text = font.render(f"Turn n°{turn}", True, (255, 255, 255))
    len = text.get_width()
    screen.blit(text, (width // 2 - len // 2, 10))
    text = font.render(f"Player n°{player}'s turn", True, (255, 255, 255))
    len = text.get_width()
    if player == 0:
        screen.blit(text, (width // 2 - len // 2, board_loc[0][0][1] - radius - 100))
    elif player == 1:
        screen.blit(text, (width // 2 - len // 2, board_loc[1][0][1] + radius + 100))
    for i in range(2):
        for j in range(6):
            center_x, center_y = board_loc[i][j]
            pygame.draw.circle(screen, (50 * i, 0, 0), (center_x, center_y), radius)
            font = pygame.font.SysFont(font_sys, 100)
            text = font.render(f"{board[i][j]}", True, (255, 255, 255))
            len = text.get_width()
            screen.blit(text, (center_x - len // 2, center_y - 25))
    for i in range(2):
        center_x = width // 2 + (i - 0.5) * radius * 17
        center_y = height // 2
        pygame.draw.circle(screen, (50 * i, 0, 0), (center_x, center_y), radius)
        font = pygame.font.SysFont(font_sys, 100)
        text = font.render(f"{attic[i]}", True, (255, 255, 255))
        len = text.get_width()
        screen.blit(text, (center_x - len // 2, center_y - 25))
    pygame.display.update()

def sow(player):
    sowing = True
    harvest = False
    while sowing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for j in range(len(board_loc[player])):
                    x, y = board_loc[player][j]
                    distance = math.sqrt((pos[0] - x)**2 + (pos[1] - y)**2)
                    if distance <= radius:
                        nb_sows = board[player][j]
                        board[player][j] = 0
                        if player == 0:
                            start_idx = 5 - j
                        elif player == 1:
                            start_idx = player * 6 + j
                        next_index = start_idx
                        for _ in range(nb_sows):
                            if player == 0:
                                next_index = (next_index + 1) % 12
                                if next_index == start_idx:
                                    next_index = (next_index + 1) % 12
                                board[rotation[next_index][0]][rotation[next_index][1]] += 1
                            elif player == 1:
                                next_index = (next_index + 1) % 12
                                if next_index == start_idx:
                                    next_index = (next_index + 1) % 12
                                board[rotation[next_index][0]][rotation[next_index][1]] += 1
                            update_screen(player, turn)
                            time.sleep(0.2)
                        sowing = False
                        if (player == 0 and next_index % 12 > 5) or (player == 1 and next_index % 12 < 6):
                            if board[rotation[next_index][0]][rotation[next_index][1]] == 2 or board[rotation[next_index][0]][rotation[next_index][1]] == 3:
                                harvest = True
                                print("harvest")
                                break
    return harvest, next_index

def harvest(player, last_index):
    count = 0
    while board[rotation[last_index][0]][rotation[last_index][1]] == 2 or board[rotation[last_index][0]][rotation[last_index][1]] == 3:
        count += board[rotation[last_index][0]][rotation[last_index][1]]
        board[rotation[last_index][0]][rotation[last_index][1]] = 0
        last_index = (last_index - 1) % 12
        update_screen(player, turn)
        time.sleep(0.2)
    attic[player] += count

def game_over(player):
        if sum(board[0]) == 0 or sum(board[1]) == 0:
            if attic[0] > attic[1]:
                player = 0
            elif attic[0] < attic[1]:   
                player = 1
            screen.fill((150, 70, 30))
            font = pygame.font.SysFont(font_sys, 200)
            text = font.render(f"Player n°{player} won !", True, (255, 255, 255))
            len = text.get_width()
            screen.blit(text, (width // 2 - len // 2, 100))
            for i in range(2):
                for j in range(6):
                    center_x, center_y = board_loc[i][j]
                    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius)
                    font = pygame.font.SysFont(font_sys, 100)
                    text = font.render(f"{board[i][j]}", True, (255, 255, 255))
                    len = text.get_width()
                    screen.blit(text, (center_x - len // 2, center_y - 25))
            pygame.display.update()
        else :
            return False
        while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        return True

# Game initialization
player = random.randint(0, 1)
turn = 0

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    update_screen(player, turn)
    harvest_possible, last_index = sow(player)
    if harvest_possible:
        harvest(player, last_index)
    if game_over(player):
        break
    turn += 1
    player = (player + 1) % 2