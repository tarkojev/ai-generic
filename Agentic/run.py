#!/usr/bin/env python3
import os
import sys
import importlib
import inspect
import json
import copy

# Ensure we can always find config.json, Agents/ and Environments/ no matter where we launch
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)


def load_class(dotted_path):
    """
    Load a class from a module given its full dotted path,
    e.g. "Agents.simplereflex.SimpleReflexAgent"
    """
    module_path, class_name = dotted_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def run_task(env_class_path, agent_class_path, grid_size, max_steps):
    EnvironmentClass = load_class(env_class_path)
    AgentClass       = load_class(agent_class_path)

    env   = EnvironmentClass(grid_size)
    agent = AgentClass()

    print(f"\n=== Running: {agent_class_path} on {env_class_path} ===")
    env.display_grid()
    steps = 0
    path  = [env.agent_position]

    # Main loop
    while getattr(env, 'treasures', []) and steps < max_steps:
        # Inspect the bound method's signature (self is already bound, so it's dropped)
        sig      = inspect.signature(agent.select_action)
        n_params = len(sig.parameters)

        if n_params == 0:
            # def select_action(self)
            action = agent.select_action()
        elif n_params == 1:
            # def select_action(self, env)
            action = agent.select_action(env)
        elif n_params == 2:
            # def select_action(self, position, env)
            action = agent.select_action(env.agent_position, env)
        else:
            raise TypeError(f"Unsupported select_action signature: {sig}")

        # Stop signal
        if action in [None, 'No Treasures left']:
            break

        moved = env.move_agent(action)
        if moved:
            path.append(env.agent_position)

        # Optional enemy moves
        if hasattr(env, 'move_enemies'):
            env.move_enemies()

        steps += 1
        # Check if agent died
        if hasattr(env, 'alive') and not env.alive:
            break

    # Summary
    print(f"Steps: {steps}, Score: {getattr(env, 'score', 0)}")
    print(f"Path: {path}")
    if hasattr(env, 'alive') and not env.alive:
        print("Result: Agent died.")
    elif not getattr(env, 'treasures', []):
        print("Result: All treasures collected.")
    else:
        print("Result: Max steps reached or agent stopped.")


def main():
    config_path = os.path.join(SCRIPT_DIR, "config.json")
    with open(config_path, "r") as f:
        config = json.load(f)

    for task in config.get("tasks", []):
        run_task(
            env_class_path   = task["environment"],
            agent_class_path = task["agent"],
            grid_size        = task.get("grid_size", 5),
            max_steps        = task.get("max_steps", 100)
        )


if __name__ == "__main__":
    main()
