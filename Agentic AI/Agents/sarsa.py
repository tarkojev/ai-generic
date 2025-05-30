#!/usr/bin/env python3

# SARSA Agent uses SARSA to learn the optimal policy for the grid world
"""
SARSA is an on-policy reinforcement learning algorithm that updates the Q-values based on the action taken and the next action selected.
It stands for State-Action-Reward-State-Action. 
The agent learns the value of the action taken in the current state and updates its Q-values accordingly.
"""

import random  # For random number generation

class SARSAAgent:
    def __init__(self):
        self.q_table = {}
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 0.1  # Exploration rate

    # Selects an action based on the current environment
    def select_action(self, env):
        if random.random() < self.epsilon:
            return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        else:
            state = env.agent_position
            if state not in self.q_table:
                self.q_table[state] = [0, 0, 0, 0]  # Initialize Q-values for UP, DOWN, LEFT, RIGHT
            return ['UP', 'DOWN', 'LEFT', 'RIGHT'][self.q_table[state].index(max(self.q_table[state]))]
    # Updates the Q-table based on the action taken and the reward received
    def update_q_table(self, state, action, reward, next_state, next_action):
        if state not in self.q_table:
            self.q_table[state] = [0, 0, 0, 0]
        if next_state not in self.q_table:
            self.q_table[next_state] = [0, 0, 0, 0]
        action_index = ['UP', 'DOWN', 'LEFT', 'RIGHT'].index(action)
        next_action_index = ['UP', 'DOWN', 'LEFT', 'RIGHT'].index(next_action)
        self.q_table[state][action_index] += self.alpha * (reward + self.gamma * self.q_table[next_state][next_action_index] - self.q_table[state][action_index])
    # Resets the Q-table
    def reset_q_table(self):
        self.q_table = {}
    # Displays the Q-table
    def display_q_table(self):
        for state, q_values in self.q_table.items():
            print(f"State: {state}, Q-values: {q_values}")
