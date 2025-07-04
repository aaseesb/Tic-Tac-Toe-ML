from random import randint, random
from numpy import argmax
from pickle import load, dump
from os import remove, path

# GAME
class TicTacToe:
    def __init__(self, players):
        self.players = players
        self.reset()
    
    def reset(self):
        self.board = [" " for x in range(9)]
        self.done = False
        self.winner = ''
        self.win_cells = None;

    def aigame(self):
        while True:
            move = self.players[0].step_ai(self)
            self.board[move] = "X"
            self.check_win()
            if self.done:
                break

            move = self.players[1].step_ai(self)
            self.board[move] = "O"
            self.check_win()
            if self.done:
                break

    def available_actions(self, board):
        actions = []
        for i in range(9):
            if board[i] == ' ':
                actions.append(i)
        return actions
        
    def check_win(self):
        winconditions = [(0,1,2),(3,4,5),(6,7,8),
                         (0,3,6),(1,4,7),(2,5,8),
                         (0,4,8),(2,4,6)]
        for (a,b,c) in winconditions:
            if self.board[a] != " " and self.board[a]==self.board[b]==self.board[c]:
                self.win_cells = (a,b,c)
                self.done = True
                if self.board[a] == "X":
                    self.winner = 0
                    return self.winner
                else:
                    self.winner = 1
                    return self.winner
        # check for draws must occur after all checks for winners (board can be full and still have a winner)
        if " " not in self.board:
            self.done = True
            self.winner = 2
            return self.winner
        return None


# PLAYER
class Player:
    def __init__(self, name, epsilon = 0.5, alpha = 0.1, gamma = 0.9, q_table = {}):
        self.name =  name
        self.q_table = q_table
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.last_state = None
        self.last_action = None
        

    def step_ai(self, env):
        validmoves = env.available_actions(env.board)
        state = tuple(env.board)

        if state not in self.q_table:
            self.q_table[state] = [0 for x in range(len(validmoves))]
        
        #epsilon-greedy policy
        if random() < self.epsilon:
            move_index = randint(0,len(validmoves)-1)
        
        else:
            move_index = argmax(self.q_table[state])
        move = validmoves[move_index]

        if self.last_state is not None:
            self.update_q_value(env, self.last_state,self.last_action,0,state,False)
        
        self.last_state = state
        self.last_action = move_index
        return move
    

    def update_q_value(self, env, state, action_index, reward, next_state, done):
        current_q = self.q_table[state][action_index]
        if done:
            target = reward
        else:
            next_validmoves = env.available_actions(next_state)
            if tuple(next_state) not in self.q_table:
                self.q_table[tuple(next_state)] = [0 for x in range(len(next_validmoves))]
            target = reward + self.gamma * max(self.q_table[tuple(next_state)])

        self.q_table[state][action_index] += self.alpha * (target - current_q)
    

    def final_update(self, reward, env):
            if self.last_state is not None:
                self.update_q_value(env, self.last_state, self.last_action, reward, None, True)
                self.last_state = None
                self.last_action = None

def training(env, p1,p2, episodes):
    for i in range(episodes):
        env.aigame()
        winner = env.check_win()
        if winner == 0:
            p1.final_update(1, env)
            p2.final_update(-1, env)
        elif winner == 1:
            p1.final_update(-1,env)
            p2.final_update(1, env)
        else:
            p1.final_update(0.5, env)
            p2.final_update(0.5, env)


        env.reset()

def check(env, p1,p2):
    win, loss, draw = 0,0,0
    for i in range(100000):
        env.aigame()
        winner = env.check_win()
        if winner == 0:
            win += 1
            p1.final_update(1, env)
            p2.final_update(-1, env)
        elif winner == 1:
            loss+=1
            p1.final_update(-1, env)
            p2.final_update(1, env)
        else:
            draw+=1
            p1.final_update(0.5, env)
            p2.final_update(0.5, env)
        
        env.reset()
    return win, loss, draw

def get_qvalues(x_ai, o_ai, env, turn):
    board = tuple(env.board)
    
    if turn == 'X':
        q_table = x_ai.q_table
    elif turn == 'O':
        q_table = o_ai.q_table

    x = q_table[board] if board in q_table else []
    
    return [round(i,3) for i in x]

def clear_dict(dictionary_filenames):
    for file in dictionary_filenames:
        if path.exists(file):
            remove(file)

def save_dict(dictionary, filename):
    with open(filename, 'wb') as f:
        dump(dictionary, f)

def load_dict(filename):
    with open(filename, 'rb') as f:
        return load(f)