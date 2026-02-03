import numpy as np # type: ignore
import random

class QAgent:
    def __init__(self, rows, cols):
        self.q_table = np.zeros((rows, cols, 4)) # 4 ACTIONS, CARDINAL DIRECTIONS
        self.lr = 0.1          # LEARNING RATE
        self.gamma = 0.9       # CARE ABOUT FUTURE REWARDS
        self.epsilon = 1.0     # EXPLORATION RATIO
        self.decay = 0.995     # RATE IT STOPS BEING RANDOM

    def get_action(self, state):
        # Epsilon-Greedy logic
        if random.random() < self.epsilon:
            return random.randint(0, 3) # Choose random direction
        return np.argmax(self.q_table[state[0], state[1]])

    def update(self, state, action, reward, next_state):
        # The Bellman Equation
        old_value = self.q_table[state[0], state[1], action]
        next_max = np.max(self.q_table[next_state[0], next_state[1]])
        
        # New Q-value = (1-lr) * old + lr * (reward + gamma * best_next_step)
        self.q_table[state[0], state[1], action] = (1 - self.lr) * old_value + self.lr * (reward + self.gamma * next_max)