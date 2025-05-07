# Hybrid Agent combines the features of the various agents to make decisions

import random
from Agents.simplereflex import SimpleReflexAgent
from Agents.modelbasedreflex import ModelBasedReflexAgent
from Agents.goalbased import GoalBasedAgent
from Agents.utilitybased import UtilityBasedAgent
from Agents.q_learning import QLearningAgent as LearningAgent

class HybridAgent:
    def __init__(self):
        self.simple_reflex_agent = SimpleReflexAgent()
        self.model_based_reflex_agent = ModelBasedReflexAgent()
        self.goal_based_agent = GoalBasedAgent()
        self.utility_based_agent = UtilityBasedAgent()
        self.learning_agent = LearningAgent()

    def select_action(self, env):
        for agent in [
            lambda e: self.simple_reflex_agent.select_action(),
            lambda e: self.model_based_reflex_agent.select_action(e.agent_position, e),
            lambda e: self.goal_based_agent.select_action(e),
            lambda e: self.utility_based_agent.select_action(e),
            lambda e: self.learning_agent.select_action(e),
        ]:
            try:
                action = agent(env)
                if action and action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                    return action
            except:
                continue
        return 'No valid actions left'

    def update_q_table(self, *args, **kwargs):
        self.learning_agent.update_q_table(*args, **kwargs)

    def reset_q_table(self):
        self.learning_agent.reset_q_table()

    def display_q_table(self):
        self.learning_agent.display_q_table()
