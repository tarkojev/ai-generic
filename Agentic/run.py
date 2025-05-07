import importlib
import json
import copy
import heapq  # To enable priority queue functionality where the smallest value is always first.
from collections import deque  # Queuing from both front and back ends as either FIFO or LIFO.

# This script runs a series of tasks defined in a config.json file.
def load_class(dotted_path):
    module_path, class_name = dotted_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

# This function runs a task by loading the environment and agent classes, creating instances of them, and executing the agent's actions in the environment.
def run_task(env_class_path, agent_class_path, grid_size, max_steps):
    EnvironmentClass = load_class(env_class_path)
    AgentClass = load_class(agent_class_path)

    env = EnvironmentClass(grid_size)
    agent = AgentClass()

    print(f"\n=== Running: {agent_class_path} on {env_class_path} ===")
    env.display_grid()
    steps = 0
    path = [env.agent_position]

    # Main loop: run until all treasures are collected or max steps reached
    while getattr(env, 'treasures', []) and steps < max_steps:
        # Choose action
        try:
            action = agent.select_action(env)
        except TypeError:
            action = agent.select_action(env.agent_position, env)

        if action in ['No Treasures left', None]:
            break

        # Apply action
        moved = env.move_agent(action)

        # Optional: move enemies
        if hasattr(env, 'move_enemies'):
            env.move_enemies()

        # Update path and step counter
        if moved:
            path.append(env.agent_position)

        steps += 1

        # Check if agent is dead
        if hasattr(env, 'alive') and not env.alive:
            break

    # Final status
    print(f"Steps: {steps}, Score: {getattr(env, 'score', 0)}")
    print(f"Path: {path}")

    if hasattr(env, 'alive') and not env.alive:
        print("Result: Agent died.")
    elif not getattr(env, 'treasures', []):
        print("Result: All treasures collected.")
    else:
        print("Result: Max steps reached or agent stopped.")

def main():
    with open("config.json", "r") as f:
        config = json.load(f)

    for task in config["tasks"]:
        run_task(
            env_class_path=task["environment"],
            agent_class_path=task["agent"],
            grid_size=task.get("grid_size", 5),
            max_steps=task.get("max_steps", 100)
        )

if __name__ == "__main__":
    main()