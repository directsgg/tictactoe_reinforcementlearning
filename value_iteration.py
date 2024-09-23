import numpy as np
import pickle

BOARD_ROWS = 3
BOARD_COLS = 3

class State:
    def __init__(self, p1, p2):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        self.playerSymbol = 1

    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS))
        return self.boardHash
    
    def availablePositions(self):
        positions = []
        for i in range (BOARD_ROWS):
            for j in range (BOARD_COLS):
                if self.board[i, j] == 0:
                    positions.append((i,j))
        return positions
    
    def updateState(self, position):
        self.board[position] = self.playerSymbol
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    def winner(self):
        # row
        for i in range(BOARD_ROWS):
            if sum(self.board[i,:]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i,:]) == -3:
                self.isEnd = True
                return -1
        
        # col
        for i in range(BOARD_COLS):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
        
        # diagonal
        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
        diag_sum2 = sum([self.board[i, BOARD_COLS -1 - i] for i in range(BOARD_COLS)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1
            
        # tie
        # no available positions
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        
        # not end
        self.isEnd = False
        return None
    
    # dar recompensas
    def giveReward(self):
        result = self.winner()
        
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(-0.5)
        if result == -1:
            self.p1.feedReward(-0.5)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.5)
            self.p2.feedReward(0.5) 

    def play(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Training rounds {}".format(i))

            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                # take action and update board state
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)
                # check board status if it is end
                win = self.winner()
                if win is not None:
                    # self.board()
                    # endend with p1either win or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                else:
                    # Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    # take action and update board state
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)
                    # check board status if it is end
                    win = self.winner()
                    if win is not None:
                        # self.board()
                        # endend with p1either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break
    
    def play2(self):
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
            # take action and update board state
            self.updateState(p1_action)
            self.showBoard()

            # check board status if it is end
            win = self.winner()
            if win is not None:
                if win == 1:
                    print("¡", self.p1.name, "gano el juego!")
                else:
                    print("tie!")
                self.reset()
                break
            else:
                # Player 2
                positions = self.availablePositions()
                p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                # take action and update board state
                self.updateState(p2_action)
                self.showBoard()
                # check board status if it is end
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print("¡", self.p2.name, "gano el juego!")
                    else:
                        print("tie!")
                    self.reset()
                    break

    def showBoard(self):
        # p1:x  p2:o
        for i in range(0, BOARD_ROWS):
            print('-------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = 'X'
                if self.board[i, j] == -1:
                    token = 'O'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
            print('-------------')

    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS)) 
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

   
            
class Player:
    def __init__(self, name, exp_rate=0.15):
        self.name = name
        self.states = [] # recordar todas las posiciones tomadas
        self.exp_rate = exp_rate
        self.gamma = 0.9
        self.states_value = {} # state -> value

    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                # print("Value", value)
                if value >= value_max:
                    value_max = value
                    action = p
                # print("{} takes action {}".format(self.name, action))
        return action
    
    def addState(self, state):
        self.states.append(state)

    # al final del juego, actualizar el estado-valor con la funcion de iteracion de valores
    # para la mejora de la politica
    def feedReward(self, reward):
        # print("states", self.name, self.states)
        # print("reward", reward)
        next_state = None
        for state in reversed(self.states):
            max_value = float('-inf')
            value = reward + self.gamma * self.states_value.get(next_state, 0)
            max_value = max(max_value, value)
            self.states_value[state] = max_value
            reward = 0
            next_state = state
            # print("states_value", state, max_value)
            # input("Presione una tecla para continuar...")
        # print("policy: states_value", self.states_value)

    def getHash(self, board):
        boardHash = str(board.reshape(BOARD_COLS * BOARD_ROWS))
        return boardHash
    
    def reset(self):
        self.states=[]

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()
    
    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()

class HumanPlayer:
    def __init__(self, name):
        self.name = name
    
    def chooseAction(self, positions, current_board, symbol):
        while True:
            row = int(input("Ingresa en la fila:"))
            col = int(input("Ingresa en la columna:"))
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
    # part of training
    p1 = Player("p1")
    p2 = Player("p2")
    st = State(p1, p2)
    st.play(10000)  
    p1.savePolicy()
    p2.savePolicy()

    # play with human
    p1 = Player("Computer", exp_rate=0)
    p1.loadPolicy("policy_p1")
    print(len(p1.states_value))
    p2 = HumanPlayer("Human")
    st = State(p1, p2)
    st.play2()  
    