# importing the required libraries
import pygame as pg
import sys
import time
from pygame.locals import *

# declaring the global variables

# for storin the 'x' or 'o'
# value as character
XO = 'x'

# storing the winner's value at
# any instant of code
winner = None

# to check if the game is a draw
draw = None

# to set width of the game window
width = 400

# to set height of the game window
height = 400

# to set background color of the 
# game window
white = (255, 255, 255)

# color of the straightlines o that
# white game board, dividing board
# into 9 parts
line_color = (0, 0, 0)

# setting up a 3*3 board in canvas
board = [[None]*3, [None]*3, [None]*3]

# initializing the pygame window
pg.init()

# setting fps manually
fps = 30

# this is used to track time
CLOCK = pg.time.Clock()

# this method is used to buil the
# infraestructure of the display
screen = pg.display.set_mode((width, height + 100), 0, 32)

# setting up a nametag for the
# game window
pg.display.set_caption("Totito RL")

# loading the images as python object
initiating_window = pg.image.load("modified_cover.png")
x_img = pg.image.load("X_modified.png")
o_img = pg.image.load("o_modified.png")

# resizing images
initiating_window = pg.transform.scale(
    initiating_window, (width, height + 100)
)
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))

def game_initiating_window():
    # displaying over the screen
    screen.blit(initiating_window, (0, 0))
    
	# updating the display
    pg.display.update()
    time.sleep(3)
    screen.fill(white)
    
	# drawing vertical lines
    pg.draw.line(screen, line_color, (width / 3, 0),
                 (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0),
                 (width / 3 * 2, height), 7)
    
	# drawing horizontal lines
    pg.draw.line(screen, line_color, (0, height / 3),
                 (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2),
                 (width, height / 3 * 2), 7)
    
    draw_status()
    
def draw_status():
    # getting the global variable draw
    # into action
    global draw
    
    if winner is None:
        message = "Turno de " + XO.upper()
    else:
        message = "Gano " + winner.upper()

    if draw:
        message = "Game Draw" 

    # setting a font object
    font = pg.font.Font(None, 30)

    # setting the font propterties like
    # color and width of the text
    text = font.render(message, 1, (255, 255, 255))

    # copy the rendered message onto the board 
    # creating a small block at the bottom of the main display
    screen.fill((0, 0, 0), (0, 400, 500 ,100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()

def check_win():
    global board, winner, draw

    # checking for winning rows
    for row in range(0, 3):
        if ((board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None)):
            winner = board[row][0]
            pg.draw.line(screen, (250, 0, 0),
                         (0, (row + 1) * height / 3 - height / 6),
                         (width, (row + 1) * height / 3 - height / 6),
                         7)
            break
    
    # checking for winning rows
    for col in range(0, 3):
        if ((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None)):
            winner = board[0][col]
            pg.draw.line(screen, (250, 0, 0),
                         ((col + 1) * width / 3 - width / 6, 0),
                         ((col + 1) * width / 3 - width / 6, height),
                         7)
            break
    
    # check for diagonal winners
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
 
        # game won diagonally left to right
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)
 
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
 
        # game won diagonally right to left
        winner = board[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)
 
    if(all([all(row) for row in board]) and winner is None):
        draw = True

    draw_status()

def drawXO(row, col):
    global board, XO
    # for the first row, the image
    # should be pasted at a x coordinate
    # of 30 from the left margin
    if row == 1:
        posx = 30

    # for the second row, the image
    # should be pasted at a x coordinate
    # of 30 from the game line
    if row == 2:
        # margin or widht / 3 + 30 from
        # the left margin of the window
        posx = width / 3 + 30
    
    if row == 3:
        posx = width / 3 * 2 + 30
    
    if col == 1:
        posy = 30
        
    if col == 2:
        posy = height / 3 + 30
    
    if col == 3:
        posy = height / 3 * 2 + 30

    # setting up the required board
    # value to display
    board[row-1][col-1] = XO

    if (XO == 'x'):
        # pasting x_img over the screen 
        # at a coordinate position of
        # (posy, posx) defined in the
        # above code
        screen.blit(x_img, (posy, posx))
        XO = 'o'
    else:
        screen.blit(o_img, (posy, posx))
        XO = 'x'
    pg.display.update()

def user_click():
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()

    # get column of mouse click (1-3)
    if (x < width / 3):
        col = 1
    elif (x < width / 3 * 2):
        col = 2
    elif (x < width):
        col = 3
    else: 
        col = None

    # get row of mouse click
    if (y < height / 3):
        row = 1
    elif (y < height / 3 * 2):
        row = 2
    elif (y < height):
        row = 3
    else:
        row = None
    
    # after getting the row and col,
    # we need to draw the images at
    # the desired positions
    if (row and col and board[row-1][col-1] is None):
        global XO
        drawXO(row, col)
        check_win()

def reset_game():
    global board, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    game_initiating_window()
    winner = None
    board = [[None]*3, [None]*3, [None]*3]

game_initiating_window()
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            user_click()
            if(winner or draw):
                reset_game()
    pg.display.update()
    CLOCK.tick(fps)




# import pygame
# import sys

# # Inicializar Pygame
# pygame.init()

# # Configuración de la pantalla
# screen = pygame.display.set_mode((600, 400))
# pygame.display.set_caption("Menú Principal")

# # Colores
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# BLUE = (0, 0, 255)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)

# # Fuente
# font = pygame.font.Font(None, 40)

# # Opciones del menú
# menu_options = ["Jugar contra RL", "Entrenar agente", "Opciones", "Salir"]
# selected_option = 0

# def draw_menu():
#     screen.fill(WHITE)
#     for i, option in enumerate(menu_options):
#         color = BLUE if i == selected_option else BLACK
#         text = font.render(option, True, color)
#         text_rect = text.get_rect(center=(300, 100 + i * 60))
#         screen.blit(text, text_rect)
#     pygame.display.flip()

# # Bucle principal del juego
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP:
#                 selected_option = (selected_option - 1) % len(menu_options)
#             elif event.key == pygame.K_DOWN:
#                 selected_option = (selected_option + 1) % len(menu_options)
#             elif event.key == pygame.K_RETURN:
#                 if selected_option == 0:
#                     print("Jugar contra RL seleccionado")
#                 elif selected_option == 1:
#                     print("Entrenar agente seleccionado")
#                 elif selected_option == 2:
#                     print("Opciones seleccionado")
#                 elif selected_option == 3:
#                     pygame.quit()
#                     sys.exit()

#     draw_menu()
