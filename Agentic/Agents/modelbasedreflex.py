#!/usr/bin/env python3

# Model-Based Reflex Agent moves randomly but remembers past visits
import random

class ModelBasedReflexAgent:
    def __init__(self):
        self.visited = set()

    # Selects an action based on the current position and environment
    def select_action(self, position, env):
        self.visited.add(position)
        possible_actions = self.get_possible_actions(position, env)
        unvisited_actions = []
        for action in possible_actions:
            new_pos = self.get_new_position(position, action)
            if new_pos not in self.visited:
                unvisited_actions.append(action)
        if unvisited_actions:
            return random.choice(unvisited_actions)
        else:
            return random.choice(possible_actions)

    # Get possible actions based on the current position
    def get_possible_actions(self, position, env):
        actions = []
        x, y = position  # Axis
        if x > 0:
            actions.append('UP')
        if x < env.size - 1:
            actions.append('DOWN')
        if y > 0:
            actions.append('LEFT')
        if y < env.size - 1:
            actions.append('RIGHT')
        return actions

    # Get new position based on the action taken
    def get_new_position(self, position, action):
        x, y = position
        if action == 'UP':
            return (x - 1, y)
        elif action == 'DOWN':
            return (x + 1, y)
        elif action == 'LEFT':
            return (x, y - 1)
        elif action == 'RIGHT':
            return (x, y + 1)