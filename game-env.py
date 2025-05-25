import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.full((3,3)," ")
        self.done = False

    def hash_state(self):
        return ''.join(self.board.flatten())
    
    def available_actions(self):
        actions = []
        for i in range(9):
            if self.board[i//3][i%3] == '':
                actions.append(i)
        return actions
    
    def check_win(self,player):
        for i in range(3):
            if all(self.board[i, :] == player) or all(self.board[:,i] == player):
                print(1)
                return True
        
        diagnol = []
        diagnol_inv = []
        for i in range(3):
            diagnol.append(self.board[i,i])
            diagnol_inv.append(self.board[i,2-i])
        if all(entry == player for entry in diagnol) or all(entry == player for entry in diagnol_inv):
            return True
        return False
    
    def step(self, action, player):
        
        self.board[action // 3][action % 3] = player

        if self.check_win(player):
            self.done = True
            print('player:',player,'has won')
            return True
        
    def print_board(self):
        for row in self.board:
            print(" | ".join(row))
            print('-'*10)
        
        
"""
game = TicTacToe()
game.step(0,"X")
game.step(4,"X")
game.step(8,"X")
game.print_board()
"""