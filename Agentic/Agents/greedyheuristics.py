#!/usr/bin/env python3

# Greedy Agent uses a heuristic to find the shortest path to the nearest treasure

"""
Greedy Agent uses a heuristic to find the shortest path to the nearest treasure
"""

import heapq  # For priority queue in A* algorithm

class GreedyAgent:
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
    # Finds the path to the nearest treasure using a greedy approach
    def find_path_to_nearest_treasure(self, env):
        start = env.agent_position
        treasures = env.treasures.copy()
        nearest_treasure = min(treasures, key=lambda treasure: abs(start[0] - treasure[0]) + abs(start[1] - treasure[1]))  # Lambda to fast check on each treasure location beforehand
        path = self.greedy_pathfinding(start, nearest_treasure, env)
        return path
    # Pathfinding using a greedy approach
    def greedy_pathfinding(self, start, goal, env):
        queue = []
        heapq.heappush(queue, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        while queue:
            current = heapq.heappop(queue)[1]
            if current == goal:
                return self.reconstruct_path(came_from, current)
            for action in self.get_possible_actions(current, env):
                neighbor = self.get_new_position(current, action)
                if not env.is_valid_position(neighbor) or env.grid[neighbor[0]][neighbor[1]] == 'O':
                    continue
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in queue]:
                        heapq.heappush(queue, (f_score[neighbor], neighbor))
        return []
    # Heuristic function for greedy approach
    # This is a simple heuristic that calculates the Manhattan distance between two points
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    # Reconstructs the path from the came_from dictionary
    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1][1:]  # Reverse the path and remove the start position
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