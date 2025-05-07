#!/usr/bin/env python3

import random  # Random treasures and obstacles placements on the grid. Random movements.
import copy  # To copy-deep the grid environment for different agents.
import heapq  # To enable priority queue functionality where the smallest value is always first.
from collections import deque  # Queuing from both front and back ends as either FIFO or LIFO.

"""
The TresureHunting represents a simple 2D grid-based and randomly generated environment where an agent can move around, collect treasures, and avoid obstacles.
"""

class TreasureHunting:
    def __init__(self, size):
        self.size = size
        self.grid = self.create_grid()
        self.agent_position = (0, 0)
        self.alive = True
        self.score = 0

        # For treasures: count = size → % coverage = (size / (size * size)) * 100 = (1 / size) * 100
        # For obstacles: count = int(size * 0.35) → not a true 35% coverage; it's just a rough estimate
        self.treasures = self.put_items('T', size)
        self.obstacles = self.put_items('O', int(size * 0.35))

    # Create an empty grid
    def create_grid(self):
        return [['' for _ in range(self.size)] for _ in range(self.size)]

    # Place items (T = treasure, O = obstacle) randomly on grid
    def put_items(self, item_type, count):
        positions = []
        for _ in range(count):
            while True:
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                if (x, y) != self.agent_position and self.grid[x][y] == '':
                    self.grid[x][y] = item_type
                    positions.append((x, y))
                    break
        return positions

    # Check if a position is inside the grid
    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    # Move the agent in one of four directions
    def move_agent(self, action):
        x, y = self.agent_position

        if action == 'UP':
            new_pos = (x - 1, y)
        elif action == 'DOWN':
            new_pos = (x + 1, y)
        elif action == 'LEFT':
            new_pos = (x, y - 1)
        elif action == 'RIGHT':
            new_pos = (x, y + 1)
        else:
            return False  # Invalid action

        if self.is_valid_position(new_pos):
            cell = self.grid[new_pos[0]][new_pos[1]]
            if cell != 'O':  # not an obstacle
                self.agent_position = new_pos
                # Check if the agent is on a treasure
                if cell == 'T':
                    self.score += 1
                    self.grid[new_pos[0]][new_pos[1]] = ''
                    self.treasures.remove(new_pos)
                    # Check if all treasures are collected
                    if not self.treasures:
                        self.alive = False  # stop the run if no more treasures
                # Check if the agent is on an obstacle
                return True
        return False

    # Display grid with agent, treasures and obstacles
    def display_grid(self):
        for row in range(self.size):
            grid_row = ''
            for col in range(self.size):
                pos = (row, col)
                if pos == self.agent_position:
                    grid_row += ' A '
                elif self.grid[row][col] == 'T':
                    grid_row += ' T '
                elif self.grid[row][col] == 'O':
                    grid_row += ' O '
                else:
                    grid_row += ' . '
            print(grid_row)
        print(f"Score: {self.score} | Treasures left: {len(self.treasures)} | Alive: {self.alive}")
        print()

    # Alias for display (to unify with other environments)
    def display(self):
        self.display_grid()

    # Reset environment to initial state
    def reset(self):
        self.grid = self.create_grid()
        self.agent_position = (0, 0)
        self.alive = True
        self.score = 0
        self.treasures = self.put_items('T', self.size)
        self.obstacles = self.put_items('O', int(self.size * 0.35))
        return self.grid, self.agent_position, self.treasures, self.obstacles

# Example usage
if __name__ == '__main__':
    env = TreasureHunting(5)
    env.display()
    for _ in range(10):
        action = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        print(f"Action: {action}")
        env.move_agent(action)
        env.display()
        if not env.alive:
            print("All treasures collected. Ending run.")
            break
