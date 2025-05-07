# Simple Reflex Agent moves randomly across the grid
class SimpleReflexAgent:
    def select_action(self):
        actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        return random.choice(actions)