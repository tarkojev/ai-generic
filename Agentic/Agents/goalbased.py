# Goal-Based Agent is heuristic-based and uses BFS algorithm to find the path to the nearest treasure

"""
Goal-Based Agent is heuristic-based and uses BFS algorithm to find the path to the nearest treasure.
BFS or Breadth-First Search is a graph traversal algorithm that explores all the neighbor nodes at the present depth prior to moving on to nodes at the next depth level.
"""

from collections import deque  # For deque (FIFO/LIFO queues)

class GoalBasedAgent:
    def __init__(self):
        self.path = []

    # Selects an action based on the current environment
    def select_action(self, env):
        if not self.path:
            if not env.treasures:
                return 'No Treasures left'
            self.path = self.find_path_to_nearest_treasure(env)
        if self.path:
            return self.path.pop(0)
        else:
            return 'No Treasures left'

    # Finds the path to the nearest treasure using BFS
    def find_path_to_nearest_treasure(self, env):
        start = env.agent_position
        treasures = env.treasures.copy()
        nearest_treasure = min(treasures, key=lambda treasure: abs(start[0] - treasure[0]) + abs(start[1] - treasure[1]))  # Lambda to fast check on each treasure location beforehand
        path = self.pathfinding(start, nearest_treasure, env)
        return path

    # Pathfinding using BFS(Breadth-First Search)
    def pathfinding(self, start, goal, env):
        queue = deque()
        queue.append((start, []))
        visited = set()
        while queue:
            current_position, path = queue.popleft()
            if current_position == goal:
                return path
            if current_position in visited:
                continue
            visited.add(current_position)
            for action in self.get_possible_actions(current_position, env):
                new_position = self.get_new_position(current_position, action)
                if env.is_valid_position(new_position):
                    if env.grid[new_position[0]][new_position[1]] != 'O':
                        queue.append((new_position, path + [action]))
        return []

    # Get possible actions based on the current position
    def get_possible_actions(self, position, env):
        actions = []
        x, y = position
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
