import numpy as np
import pygame

# Pygame Initialization
font_sys = "impact"
pygame.init()
screen = pygame.display.set_mode((0, 0))
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("Awale")
screen.fill((150, 70, 30))
pygame.display.update()

# Game initialization
board = np.zeros((2, 6), dtype=int)
board[0] = [4, 4, 4, 4, 4, 4]
board[1] = [4, 4, 4, 4, 4, 4]
turn = 0

# Functions
def update_screen():
    screen.fill((150, 70, 30))
    font = pygame.font.SysFont(font_sys, 100)
    text = font.render(f"Turn n°{turn}", True, (255, 255, 255))
    len = text.get_width()
    screen.blit(text, (width // 2 - len // 2, 10))
    for i in range(2):
        for j in range(6):
            radius = width // 15
            center_x = width // 2 + (j - 2.5) * radius * 2.5
            center_y = height // 2 + (i - 0.5) * radius * 2.5
            pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius)
            font = pygame.font.SysFont(font_sys, 100)
            text = font.render(f"{board[i][j]}", True, (255, 255, 255))
            len = text.get_width()
            screen.blit(text, (center_x - len // 2, center_y - 25))
    pygame.display.update()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    turn += 1
    update_screen()