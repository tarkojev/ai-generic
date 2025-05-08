#!/usr/bin/env python3

import random  # Random treasures and obstacles placements on the grid. Random movements.

"""
The PuzzleWithEnemies represents a simple 2D grid-based environment where an agent can move around, collect treasures, and interact with a switch and a door.
Moving Enemies are also present in the environment, and the agent must avoid them to survive.
"""

class PuzzleWithEnemies:
    def __init__(self, size):
        # Initializes the grid, places the agent, switch, door, treasures, and enemies.
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.agent_position = (0, 0)
        self.switch_position = self.place_item('S')
        self.door_position = self.place_item('D')
        self.treasures = self.place_items('T', 3)
        self.enemies = self.place_items('E', 2)  # 2 enemies
        self.door_open = False
        self.score = 0
        self.alive = True

    def place_item(self, item):
        # Places a single item randomly on the grid.
        while True:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (x, y) != self.agent_position and self.grid[x][y] == '':
                self.grid[x][y] = item
                return (x, y)

    def place_items(self, item, count):
        # Places multiple items randomly on the grid.
        positions = []
        for _ in range(count):
            pos = self.place_item(item)
            positions.append(pos)
        return positions

    def is_valid(self, pos):
        # Checks if a position is within the grid boundaries.
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size

    def is_valid_position(self, pos):
        # Alias for is_valid to maintain compatibility with other agents.
        return self.is_valid(pos)

    def move_agent(self, action):
        # Moves the agent in the specified direction and handles interactions with grid elements.
        if not self.alive:
            return False

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
            return False

        # Check if the new position is valid and not an obstacle.
        if self.is_valid(new_pos):
            cell = self.grid[new_pos[0]][new_pos[1]]

            if cell == 'E':
                # Agent encounters an enemy and dies.
                print("You were caught by an enemy!")
                self.alive = False
                return 'dead'

            if cell == 'D' and not self.door_open:
                # Agent tries to exit through a locked door.
                print("Door is locked! Find the switch.")
                return False
            elif cell == 'D' and self.door_open:
                # Agent exits successfully.
                print("You escaped! Level complete.")
                self.agent_position = new_pos
                self.score += 10
                return 'exit'

            if cell == 'S':
                # Agent activates the switch to open the door.
                print("Switch activated! Door is now open.")
                self.door_open = True
                self.grid[new_pos[0]][new_pos[1]] = ''
                self.score += 1

            if cell == 'T':
                # Agent collects a treasure.
                print("Collected a treasure!")
                self.treasures.remove(new_pos)
                self.grid[new_pos[0]][new_pos[1]] = ''
                self.score += 2

            # Update agent's position.
            self.agent_position = new_pos
            return True
        return False

    def move_enemies(self):
        # Moves enemies randomly on the grid.
        new_positions = []
        for pos in self.enemies:
            x, y = pos
            moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            random.shuffle(moves)
            moved = False
            for move in moves:
                if move == 'UP':
                    new_pos = (x - 1, y)
                elif move == 'DOWN':
                    new_pos = (x + 1, y)
                elif move == 'LEFT':
                    new_pos = (x, y - 1)
                elif move == 'RIGHT':
                    new_pos = (x, y + 1)

                if self.is_valid(new_pos) and self.grid[new_pos[0]][new_pos[1]] == '':
                    # Move enemy to a new valid position.
                    self.grid[x][y] = ''
                    self.grid[new_pos[0]][new_pos[1]] = 'E'
                    new_positions.append(new_pos)
                    moved = True
                    break
            if not moved:
                # Enemy stays in the same position if no valid move is found.
                new_positions.append(pos)
        self.enemies = new_positions

        if self.agent_position in self.enemies:
            # Enemy moves onto the agent, ending the game.
            print("Enemy moved onto agent! Game over.")
            self.alive = False

    def display(self):
        # Displays the current state of the grid.
        for i in range(self.size):
            row = ''
            for j in range(self.size):
                pos = (i, j)
                if pos == self.agent_position and self.alive:
                    row += ' A '
                elif self.grid[i][j] == 'T':
                    row += ' T '
                elif self.grid[i][j] == 'S':
                    row += ' S '
                elif self.grid[i][j] == 'D':
                    row += ' D '
                elif self.grid[i][j] == 'E':
                    row += ' E '
                else:
                    row += ' . '
            print(row)
        print(f"Score: {self.score}, Door Open: {self.door_open}, Alive: {self.alive}")
        print()

    def display_grid(self):
        # Alias for display to maintain compatibility with other agents.
        self.display()

    def reset(self):
        # Resets the environment to its initial state.
        self.__init__(self.size)
        return self.grid, self.agent_position, self.treasures, self.enemies

#  Example usage
if __name__ == '__main__':
    env = PuzzleWithEnemies(6)
    actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    for _ in range(100):
        env.display()
        if not env.alive:
            print("Agent died. Game over.")
            break
        
        # Randomly choose an action for the agent.
        action = random.choice(actions)
        print(f"Agent chooses: {action}")
        result = env.move_agent(action)

        # Move enemies after the agent's action.
        env.move_enemies()

        # Display the grid after the agent's and enemies' actions.
        if result == 'exit':
            print("Agent completed the level!")
            break
