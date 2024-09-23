import math
import random
import pygame
import sys



# inicializar pygame
pygame.init()

# configuracion de la pantalla
screen =pygame.display.set_mode((300, 300))
pygame.display.set_caption("Totito UI")

# colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# variables del juego
board = [[None]*3, [None]*3, [None]*3]
current_player = "X"
winner = None
game_over = False

# dibujar la cuadricula
def draw_grid():
    screen.fill(WHITE)
    for x in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, 100 * x), (300, 100 * x), 2)
        pygame.draw.line(screen, BLACK, (100 * x, 0), (100 * x, 300), 2)

# dibujar las marcas
def draw_marks():
    for y in range(3):
        for x in range(3):
            if board[y][x] == "X":
                pygame.draw.line(screen, RED, (x * 100 + 15, y * 100 + 15), (x * 100 + 85, y * 100 + 85), 2)
                pygame.draw.line(screen, RED, (x * 100 + 85, y * 100 + 15), (x * 100 + 15, y * 100 + 85), 2)
            elif board[y][x]== "O":
                #draw_hand_drawn_circle(screen, BLUE, (x * 100 + 50, y * 100 + 50), 40, 2)
                pygame.draw.circle(screen, BLUE, (x * 100 + 50, y * 100 + 50), 40, 2)        

# # dibujar un circulo con estilo dibujado a mano
def draw_hand_drawn_circle(surface, color, center, radius, width):
    for _ in range(10):
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)
        pygame.draw.circle(surface, color, (center[0]+ offset_x, center[1] + offset_y), radius, width)
# def draw_hand_drawn_circle(surface, color, center, radius, width):
#     steps = 30  # Número de pasos para la animación
#     for i in range(steps):
#         angle = (i / steps) * 2 * math.pi
#         end_angle = ((i + 1) / steps) * 2 * math.pi
#         offset_x = random.randint(-2, 2)
#         offset_y = random.randint(-2, 2)
#         pygame.draw.arc(surface, color, (center[0] - radius, center[1] - radius, 2 * radius, 2 * radius), angle, end_angle, width)
#         pygame.display.flip()
#         pygame.time.delay(3)  # Retraso para la animación
        
# verificar ganador
def check_winner():
    global winner, game_over
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            winner = row[0]
            game_over = True
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col]is not None:
            winner = board[0][col]
            game_over = True
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        winner = board[0][0]
        game_over = True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        winner = board[0][2]
        game_over = True

# bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            row, col = y // 100, x // 100
            print(row, col)
            if board[row][col] is None:
                board[row][col] = current_player
                current_player = "O" if current_player == "X" else "X"
                check_winner()
    draw_grid()
    draw_marks()
    pygame.display.flip()
