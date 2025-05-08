#!/usr/bin/env python3

# Simple Reflex Agent moves randomly across the grid
import random
class SimpleReflexAgent:
    def select_action(self):
        actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        return random.choice(actions)