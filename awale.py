import pygame
import math

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
radius = width // 15
board_loc = [[(width // 2 + (j - 2.5) * radius * 2.5, height // 2 + (i - 0.5) * radius * 2.5) for j in range(6)] for i in range(2)]
rotation = [[0, 5], [0, 4], [0, 3], [0, 2], [0, 1], [0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5]]

# Functions
def update_screen():
    screen.fill((150, 70, 30))
    font = pygame.font.SysFont(font_sys, 100)
    text = font.render(f"Turn n°{turn}", True, (255, 255, 255))
    len = text.get_width()
    screen.blit(text, (width // 2 - len // 2, 10))
    for i in range(2):
        for j in range(6):
            center_x, center_y = board_loc[i][j]
            pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius)
            font = pygame.font.SysFont(font_sys, 100)
            text = font.render(f"{board[i][j]}", True, (255, 255, 255))
            len = text.get_width()
            screen.blit(text, (center_x - len // 2, center_y - 25))
    pygame.display.update()

def seed(player):
    seeding = True
    while seeding:
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
                        nb_seeds = board[player][j]
                        board[player][j] = 0
                        for i in range(nb_seeds):
                            if player == 0:
                                next_index = (6 - j + i) % 12
                                board[rotation[next_index][0]][rotation[next_index][1]] += 1
                            elif player == 1:
                                next_index = (player * 6 + j + 1 + i) % 12
                                board[rotation[next_index][0]][rotation[next_index][1]] += 1
                        seeding = False

# Game initialization
player = 0
turn = 0

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    update_screen()
    seed(player)
    turn += 1
    update_screen()