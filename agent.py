from collections import defaultdict
import numpy as np
import random


class agent:
    def __init__(self, alpha = 0.1, gamma = 0.9, epsilon = 0.02):

        self.q_table = defaultdict(lambda: np.zeros(9))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def choose_action(self, state, available_actions):
        if random.random() < self.epsilon:
            return random.choice(available_actions)
        else:
            q_values = self.q_table[state]
            valid_choices = {action: q_values[action] for action in available_actions}
            max_q = max(valid_choices.values())
            
            best_action = [action for action, q in valid_choices.items() if q == max_q]
            return random.choice(best_action)

    def learn(self,state,action,reward,next_state, done):
        old_value = self.q_table[state][action]
        if done:
            next_max = 0
        else:
            available = self.available_actions(next_state)
            next_max = max(self.q_table[next_state][a] for a in available) # wtf is this dawg please help me
        
        self.q_table[state][action] += self.alpha * (reward + self.gamma * next_max - old_value)

#setup game env