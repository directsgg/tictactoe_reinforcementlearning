import pickle
import time
import numpy as np

import pygame
import sys

import pygame.display
import pygame.docs
import pygame.draw
import pygame.draw_py
import pygame.event
import pygame.font
import pygame.image
import pygame.mouse
import pygame.surface
import pygame.time
import pygame.transform

BOARD_ROWS = 3
BOARD_COLS = 3

#colores
WHITE = (255, 255, 255)
LINE_COLOR = (100, 100, 100)
RED = (255, 0, 0)
# BLUE = (0, 0, 255)

# configurar el objeto fuente

# se usa para seguir el tiempo
CLOCK = pygame.time.Clock()

# dimensiones de la pantalla
WIDTH = 600
HEIGHT = 600
MARGINH = int(WIDTH * 0.05)
MARGINV = int(HEIGHT * 0.05)

# imagenes
initiating_window = pygame.image.load("modified_cover.png")
x_img = pygame.image.load("x_mod.png")
o_img = pygame.image.load("o_mod.png")
# redimensionar imagenes
initiating_window = pygame.transform.scale(initiating_window, (WIDTH, HEIGHT))
x_img = pygame.transform.scale(x_img, (int(((WIDTH / 3) - MARGINH) * 0.8), int(((HEIGHT / 3) - MARGINV) *0.8)))
o_img = pygame.transform.scale(o_img, (int(((WIDTH / 3) - MARGINH) * 0.8), int(((HEIGHT / 3) - MARGINV) *0.8)))

# clase del tablero general
# que define las reglas del juego y
# actua a modo de juez al decidir quien gana el juego
# tambien dibuja el tablero
class StateBoard:
    def __init__(self):
        # el tablero al llenarse de ceros significa que esta vacio
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        # jugador 1 con el simbolo que llenara el tablero es el 1
        self.p1 = None
        # jugador 2 con el simbolo que llenara el tablero es el -1
        self.p2 = None
        self.isEnd = False
        # boardHash para generar un identificador del estado del tablero
        self.boardHash = None
        # incia jugando el jugador con el simbolo 1
        self.playerSymbol = 1
        
        # inicializar pygame
        pygame.init()
        # configuracion de la pantalla
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption("Totito RL")
        self.game_initiating_window()

    def set_player(self, player):
        if self.p1 is None and self.p2 is None:
            self.p1 = player
        elif self.p1 is not None and self.p2 is None:
            self.p2 = player

    # presentar la pantalla inicial
    def game_initiating_window(self):
        # presetarlo sobre la pantalla
        self.screen.blit(initiating_window, (0, 0))
        pygame.display.update()
        time.sleep(3)
        #
        #
        # dibujar la cuadricula
        self.screen.fill(WHITE)
        # lineas verticales
        pygame.draw.line(self.screen, LINE_COLOR, (WIDTH / 3, 0 + MARGINV + HEIGHT // 30), (WIDTH / 3, HEIGHT - MARGINV - HEIGHT // 30), 10)
        pygame.draw.line(self.screen, LINE_COLOR, (WIDTH / 3 * 2, 0 + MARGINV + HEIGHT // 30), (WIDTH / 3 * 2, HEIGHT - MARGINV - HEIGHT // 30), 10)
        # lineas horizontales
        pygame.draw.line(self.screen, LINE_COLOR, (0 + MARGINH, HEIGHT / 3), (WIDTH - MARGINH, HEIGHT / 3), 10)
        pygame.draw.line(self.screen, LINE_COLOR, (0 + MARGINH, HEIGHT / 3 * 2), (WIDTH - MARGINH, HEIGHT / 3 * 2), 10)

    # obtener el hash del tablero actual
    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS))
        return self.boardHash

    # posiciones disponibles en el tablero
    def availablePositions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions
    
    # actualizar el estado del tablero al agregar un nuevo simbolo al mismo
    def updateState(self, position):
        self.board[position] = self.playerSymbol
        # cambiar el turno del jugador
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    # juez para definir el ganador
    def winner(self):
        # verificar en las filas
        for i in range(BOARD_ROWS):
            if sum(self.board[i,:]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i,:]) == -3:
                self.isEnd = True
                return -1
            
        # verificar en las columnas
        for i in range(BOARD_COLS):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
            
        # verificar diagonales
        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
        diag_sum2 = sum([self.board[i, BOARD_COLS - 1 - i] for i in range(BOARD_COLS)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1
        
        # empate si ya no quedan posiciones disponibles
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        
        # el juego aun no ha terminado
        self.isEnd = False
        return None
    
    def playGame(self):
        # bucle principal del juego
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not self.isEnd:
                    # jugador 1
                    positions = self.availablePositions()
                    p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                            
                    # al tomar la accion actualizar el estado del tablero
                    self.updateState(p1_action)
                    print(self.board)
                    self.showBoard()
                    win = self.winner()
                    print("Ganador", win)
                    if (win is not None):
                        # verificar en las filas
                        for row in range(BOARD_ROWS):
                            sumRows = sum(self.board[row,:])
                            if sumRows == 3 or sumRows == -3:
                                pygame.draw.line(self.screen, RED, 
                                                 (0 + MARGINH + WIDTH // 20,  (row + 1) * HEIGHT / 3 - HEIGHT / 6),
                                                 (WIDTH - MARGINH - WIDTH // 20, (row + 1) * HEIGHT / 3 -HEIGHT / 6),
                                                 12)
                                break
                            
                        # verificar en las columnas
                        for col in range(BOARD_COLS):
                            sumCols = sum(self.board[:, col])
                            if  sumCols == 3 or sumCols == -3:
                                pygame.draw.line(self.screen, RED, 
                                                 ((col + 1) * WIDTH / 3 - WIDTH / 6, 0 + MARGINV + HEIGHT // 20),
                                                 ((col + 1) * WIDTH / 3 - WIDTH / 6, HEIGHT - MARGINV - HEIGHT // 20),
                                                 12)
                                break

                        # verificar diagonales
                        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
                        if diag_sum1 == 3 or diag_sum1 == -3:
                            pygame.draw.line(self.screen, RED, 
                                             (MARGINH + WIDTH // 20, MARGINV + HEIGHT // 20),
                                             (WIDTH - MARGINH - WIDTH // 20, HEIGHT - MARGINV - HEIGHT // 20),
                                             12) 
                        diag_sum2 = sum([self.board[i, BOARD_COLS - 1 - i] for i in range(BOARD_COLS)])
                        if diag_sum2 == 3 or diag_sum2 == -3:
                            pygame.draw.line(self.screen, RED, 
                                             (WIDTH - MARGINH - WIDTH // 20, MARGINV + HEIGHT // 20),
                                             (MARGINH + WIDTH // 20, HEIGHT - MARGINV - HEIGHT // 20),
                                             12)
                        pygame.display.update() 
                        self.reset_game()  
                    else:
                        # jugador 2
                        positions = self.availablePositions()
                        p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                        # al tomar la accion actualizar el estado del tablero
                        self.updateState(p2_action)
                        print(self.board)
                        self.showBoard()
                        win = self.winner()
                        if (win is not None):
                            # verificar en las filas
                            for row in range(BOARD_ROWS):
                                sumRows = sum(self.board[row,:])
                                if sumRows == 3 or sumRows == -3:
                                    pygame.draw.line(self.screen, RED, 
                                                     (0 + MARGINH + WIDTH // 20,  (row + 1) * HEIGHT / 3 - HEIGHT / 6),
                                                     (WIDTH - MARGINH - WIDTH // 20, (row + 1) * HEIGHT / 3 -HEIGHT / 6),
                                                     12)
                                    break
                                
                            # verificar en las columnas
                            for col in range(BOARD_COLS):
                                sumCols = sum(self.board[:, col])
                                if  sumCols == 3 or sumCols == -3:
                                    pygame.draw.line(self.screen, RED, 
                                                     ((col + 1) * WIDTH / 3 - WIDTH / 6, 0 + MARGINV + HEIGHT // 20),
                                                     ((col + 1) * WIDTH / 3 - WIDTH / 6, HEIGHT - MARGINV - HEIGHT // 20),
                                                     12)
                                    break
                                
                            # verificar diagonales
                            diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
                            if diag_sum1 == 3 or diag_sum1 == -3:
                                pygame.draw.line(self.screen, RED, 
                                                 (MARGINH + WIDTH // 20, MARGINV + HEIGHT // 20),
                                                 (WIDTH - MARGINH - WIDTH // 20, HEIGHT - MARGINV - HEIGHT // 20),
                                                 12) 
                            diag_sum2 = sum([self.board[i, BOARD_COLS - 1 - i] for i in range(BOARD_COLS)])
                            if diag_sum2 == 3 or diag_sum2 == -3:
                                pygame.draw.line(self.screen, RED, 
                                                 (WIDTH - MARGINH - WIDTH // 20, MARGINV + HEIGHT // 20),
                                                 (MARGINH + WIDTH // 20, HEIGHT - MARGINV - HEIGHT // 20),
                                                 12)
                            pygame.display.update() 
                            self.reset_game()

            pygame.display.update()      
            CLOCK.tick(30)
    
    def showBoard(self):
        # p1:x  p2:o
        for i in range(0, BOARD_ROWS):
            for j in range(0, BOARD_COLS):
                posx = j * (WIDTH // 3 ) + MARGINH
                posy = i * (HEIGHT // 3) + MARGINV
                if self.board[i, j] == 1:
                    # line1I = (j * 100 + 15, i * 100 + 15)
                    # line1F = (j * 100 + 85, i *100 + 85)
                    # line2I = (j * 100 + 85, i * 100 + 15)
                    # line2F = (j * 100 + 15, i *100 + 85)
                    # pygame.draw.line(self.screen, RED, line1I, line1F, 2)
                    # pygame.draw.line(self.screen, RED, line2I, line2F, 2)
                    self.screen.blit(x_img, (posx, posy))
                elif self.board[i, j] == -1:
                    self.screen.blit(o_img, (posx, posy))
                    # center = (j * 100 + 50, i * 100 + 50)
                    # pygame.draw.circle(self.screen, BLUE, center, 40, 2)  

    # resetear el estado del tablero
    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1
    
    # resetar el juego en GUI
    def reset_game(self):
        time.sleep(3)
        self.reset()
        self.game_initiating_window()
    
# clase para el agente
class Player:
    def __init__(self, state_board, name, exp_rate=0.15):
        self.name = name
        self.states = [] # recordar el estad de tableros
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {} # state -> value
        self.state_board = state_board
        # establecer referencia en stateBoard
        self.state_board.set_player(self)
    
    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # tomar una accion aleatoria
            idx = np.random.choice(len(positions))
            action = positions[idx]
        
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                if value >= value_max:
                    value_max = value
                    action = p

                    message = str(round(value, 2))
                    # configurar las propiedades de la fuente y el texto
                    font = pygame.font.Font(None, 40)
                    
                    text = font.render(message, True, (0, 0, 0), (255, 200, 200))
                    
                    # poner el mensaje renderizado en la GUI
                    posx = action[1] * (WIDTH // 3 ) + MARGINH + WIDTH // 10
                    posy = action[0] * (HEIGHT // 3) + MARGINV + HEIGHT // 10
                    text_rect = text.get_rect(center = (posx, posy))
                    self.state_board.screen.blit(text, text_rect)
                    
                    pygame.display.update()
                    pygame.time.delay(1000)
                    text = font.render(message, 1, WHITE, WHITE)
                    self.state_board.screen.blit(text, text_rect)

                print("Value: {} Action: {}".format(value, p))
        return action  

    def addState(self, state):
        self.states.append(state)

    # al final del juego, actualizar el estado-valor con la funcion de iteracion de valores
    # para la mejora de la politica
    def feedReward(self, reward):
        for state in reversed(self.states):
            if self.states_value.get(state) is None:
                self.states_value[state] = 0
            self.states_value[state] += self.lr * (self.decay_gamma * reward - self.states_value[state])
            reward = self.states_value[state]
    
    def getHash(self, board):
        boardHash = str(board.reshape(BOARD_COLS * BOARD_ROWS))
        return boardHash
    
    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()

# clase para el jugador humano
class HumanPlayer:
    def __init__(self, state_board, name):
        self.name = name
        self.state_board = state_board
        # establecer referencia en StateBoard
        self.state_board.set_player(self)
    
    def chooseAction(self, positions, current_board, symbol):
        # obtener las coordenadas cuando el usuario hace click
        y, x = pygame.mouse.get_pos()

        # obtener la fila y columna
        row, col = x //(WIDTH // 3), y // (HEIGHT // 3)
        action = (row, col)
        if action in positions:
            return action
    
    def addState(self, state):
        pass

    def feedReward(self, reward):
        pass
    
    def reset(self):
        pass


if __name__ == "__main__":
    stBoard = StateBoard()
    p1 = HumanPlayer(stBoard, "Humano2jaja")
    p2 = Player(stBoard, "Computadora", exp_rate=0)
    p2.loadPolicy("policy_p2")
    stBoard.playGame()

    