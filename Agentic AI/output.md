# Input
```bash
python3 run.py
```

# Output of SAT run
```bash
=== Running: Agents.simplereflex.SimpleReflexAgent on Environments.treasurehunting.TreasureHunting ===

 A  T  .  T  . 
 .  .  .  .  . 
 .  T  O  T  T 
 .  .  .  .  . 
 .  .  .  .  . 

Score: 0 | Treasures left: 5 | Alive: True

Steps: 100, Score: 5
Path: [(0, 0), (0, 1), (1, 1), (1, 0), (2, 0), (3, 0), (2, 0), (2, 1), (1, 1), (2, 1), (1, 1), (0, 1), (0, 0), (1, 0), (0, 0), (1, 0), (2, 0), (2, 1), (2, 0), (1, 0), (1, 1), (0, 1), (1, 1), (0, 1), (0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (4, 2), (4, 1), (4, 0), (4, 1), (4, 2), (3, 2), (3, 1), (3, 0), (4, 0), (3, 0), (3, 1), (2, 1), (1, 1), (1, 2), (1, 1), (2, 1), (1, 1), (0, 1), (0, 0), (1, 0), (2, 0), (1, 0), (1, 1), (0, 1), (1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (1, 2), (1, 1), (1, 2), (1, 3), (1, 2), (0, 2), (1, 2), (0, 2), (0, 3), (0, 4), (1, 4), (1, 3), (2, 3), (2, 4)]
Result: Agent died.

=== Running: Agents.simplereflex.SimpleReflexAgent on Environments.puzzlewithenemies.PuzzleWithEnemies ===

 A  E  .  .  . 
 .  .  .  .  T 
 .  .  .  T  S 
 .  .  .  .  . 
 T  .  .  E  D 

Score: 0, Door Open: False, Alive: True

Enemy moved onto agent! Game over.
Steps: 1, Score: 0
Path: [(0, 0)]
Result: Agent died.

=== Running: Agents.modelbasedreflex.ModelBasedReflexAgent on Environments.treasurehunting.TreasureHunting ===

 A  .  .  .  T 
 .  .  T  .  O 
 .  .  T  .  T 
 T  .  .  .  . 
 .  .  .  .  . 

Score: 0 | Treasures left: 5 | Alive: True

Steps: 20, Score: 5
Path: [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4), (2, 3), (3, 3), (3, 2), (2, 2), (1, 2), (1, 1), (0, 1), (0, 2), (0, 3), (0, 4)]
Result: Agent died.

=== Running: Agents.modelbasedreflex.ModelBasedReflexAgent on Environments.puzzlewithenemies.PuzzleWithEnemies ===

 A  .  S  .  D 
 .  .  .  E  . 
 T  .  .  .  . 
 .  .  .  .  . 
 E  .  T  T  . 

Score: 0, Door Open: False, Alive: True

Enemy moved onto agent! Game over.
Steps: 5, Score: 0
Path: [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (2, 3)]
Result: Agent died.

=== Running: Agents.goalbased.GoalBasedAgent on Environments.treasurehunting.TreasureHunting ===

 A  .  .  .  . 
 .  T  .  .  . 
 T  .  T  .  . 
 T  O  .  .  . 
 .  .  .  .  T 

Score: 0 | Treasures left: 5 | Alive: True

Steps: 12, Score: 5
Path: [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0), (3, 0), (2, 0), (2, 1), (2, 2), (3, 2), (4, 2), (4, 3), (4, 4)]
Result: Agent died.

=== Running: Agents.goalbased.GoalBasedAgent on Environments.puzzlewithenemies.PuzzleWithEnemies ===

 A  .  .  .  . 
 .  .  .  T  . 
 .  .  .  .  . 
 T  .  .  E  D 
 .  E  T  .  S 

Score: 0, Door Open: False, Alive: True

Collected a treasure!
You were caught by an enemy!
Steps: 4, Score: 2
Path: [(0, 0), (1, 0), (2, 0), (3, 0), (3, 0)]
Result: Agent died.

=== Running: Agents.utilitybased.UtilityBasedAgent on Environments.treasurehunting.TreasureHunting ===

 A  .  .  .  T 
 .  .  T  .  . 
 .  .  T  .  . 
 T  .  .  .  T 
 .  .  .  O  . 

Score: 0 | Treasures left: 5 | Alive: True

Steps: 100, Score: 0
Path: [(0, 0)]
Result: Max steps reached or agent stopped.

=== Running: Agents.utilitybased.UtilityBasedAgent on Environments.puzzlewithenemies.PuzzleWithEnemies ===

 A  .  S  .  T 
 .  .  .  .  . 
 .  .  .  .  E 
 E  T  .  .  . 
 D  .  .  .  T 

Score: 0, Door Open: False, Alive: True

Enemy moved onto agent! Game over.
Steps: 5, Score: 0
Path: [(0, 0)]
Result: Agent died.

=== Running: Agents.greedyheuristics.GreedyAgent on Environments.treasurehunting.TreasureHunting ===

 A  T  .  .  . 
 .  O  .  T  . 
 .  T  .  .  . 
 .  T  .  .  . 
 T  .  .  .  . 

Score: 0 | Treasures left: 5 | Alive: True

Steps: 100, Score: 0
Path: [(0, 0)]
Result: Max steps reached or agent stopped.

=== Running: Agents.greedyheuristics.GreedyAgent on Environments.puzzlewithenemies.PuzzleWithEnemies ===

 A  .  .  .  D 
 .  .  .  E  S 
 .  .  .  .  E 
 .  .  .  .  . 
 .  T  T  .  T 

Score: 0, Door Open: False, Alive: True

Enemy moved onto agent! Game over.
Steps: 8, Score: 0
Path: [(0, 0)]
Result: Agent died.

=== Running: Agents.a_star.AStarAgent on Environments.treasurehunting.TreasureHunting ===

 A  T  .  .  T 
 .  .  .  .  . 
 T  .  .  .  . 
 .  .  O  .  . 
 .  T  T  .  . 

Score: 0 | Treasures left: 5 | Alive: True

Steps: 100, Score: 0
Path: [(0, 0)]
Result: Max steps reached or agent stopped.

=== Running: Agents.a_star.AStarAgent on Environments.puzzlewithenemies.PuzzleWithEnemies ===

 A  .  .  .  . 
 .  .  D  .  T 
 T  .  .  .  E 
 E  .  .  .  . 
 .  .  .  T  S 

Score: 0, Door Open: False, Alive: True

Enemy moved onto agent! Game over.
Steps: 11, Score: 0
Path: [(0, 0)]
Result: Agent died.

=== Running: Agents.q_learning.QLearningAgent on Environments.treasurehunting.TreasureHunting ===

 A  .  .  .  T 
 .  T  .  T  . 
 .  .  .  .  T 
 .  .  .  O  T 
 .  .  .  .  . 

Score: 0 | Treasures left: 5 | Alive: True

Steps: 100, Score: 1
Path: [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0), (1, 0), (0, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 1)]
Result: Max steps reached or agent stopped.

=== Running: Agents.q_learning.QLearningAgent on Environments.puzzlewithenemies.PuzzleWithEnemies ===

 A  D  E  .  T 
 .  .  .  .  . 
 T  .  .  .  . 
 .  .  .  .  T 
 .  E  .  .  S 

Score: 0, Door Open: False, Alive: True

Door is locked! Find the switch.
Enemy moved onto agent! Game over.
Steps: 56, Score: 0
Path: [(0, 0), (1, 0), (0, 0)]
Result: Agent died.

=== Running: Agents.sarsa.SARSAAgent on Environments.treasurehunting.TreasureHunting ===

 A  .  .  .  . 
 .  .  .  T  . 
 .  .  .  .  . 
 .  .  .  T  T 
 T  .  T  .  O 

Score: 0 | Treasures left: 5 | Alive: True

Steps: 100, Score: 0
Path: [(0, 0), (0, 1), (0, 2), (0, 1), (1, 1), (0, 1), (0, 0)]
Result: Max steps reached or agent stopped.

=== Running: Agents.sarsa.SARSAAgent on Environments.puzzlewithenemies.PuzzleWithEnemies ===

 A  .  .  T  . 
 T  E  .  .  . 
 T  .  .  D  S 
 .  .  .  E  . 
 .  .  .  .  . 

Score: 0, Door Open: False, Alive: True

Collected a treasure!
Enemy moved onto agent! Game over.
Steps: 96, Score: 2
Path: [(0, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 1), (0, 2)]
Result: Agent died.

=== Running: Agents.learningbased.LearningAgent on Environments.treasurehunting.TreasureHunting ===

 A  .  .  .  T 
 .  .  O  .  T 
 .  T  .  .  T 
 .  .  .  .  T 
 .  .  .  .  . 

Score: 0 | Treasures left: 5 | Alive: True

Steps: 100, Score: 0
Path: [(0, 0), (1, 0), (0, 0), (1, 0), (0, 0), (0, 1), (0, 0), (1, 0)]
Result: Max steps reached or agent stopped.

=== Running: Agents.learningbased.LearningAgent on Environments.puzzlewithenemies.PuzzleWithEnemies ===

 A  .  E  .  S 
 T  T  .  .  . 
 .  .  .  .  D 
 .  .  .  .  . 
 T  .  .  .  E 

Score: 0, Door Open: False, Alive: True

Enemy moved onto agent! Game over.
Steps: 20, Score: 0
Path: [(0, 0)]
Result: Agent died.

=== Running: Agents.hybridbased.HybridAgent on Environments.treasurehunting.TreasureHunting ===

 A  O  .  T  . 
 .  .  .  T  . 
 .  .  .  .  . 
 T  T  .  .  . 
 T  .  .  .  . 

Score: 0 | Treasures left: 5 | Alive: True

Steps: 100, Score: 3
Path: [(0, 0), (1, 0), (1, 1), (1, 0), (1, 1), (2, 1), (2, 0), (2, 1), (2, 0), (1, 0), (1, 1), (2, 1), (2, 2), (1, 2), (1, 1), (1, 0), (0, 0), (1, 0), (1, 1), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (3, 3), (3, 2), (4, 2), (4, 1), (4, 2), (4, 1), (4, 0), (4, 1), (4, 0), (3, 0), (4, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 2), (4, 1), (4, 2), (3, 2), (4, 2), (4, 3), (4, 4), (3, 4), (3, 3), (4, 3), (4, 4), (4, 3), (3, 3), (4, 3), (4, 2), (4, 3), (4, 2), (4, 3), (4, 2), (4, 3), (4, 4), (3, 4), (4, 4), (4, 3), (4, 4), (4, 3), (3, 3), (3, 4), (2, 4), (2, 3), (3, 3), (3, 2), (3, 1), (4, 1), (3, 1), (4, 1), (3, 1)]
Result: Max steps reached or agent stopped.

=== Running: Agents.hybridbased.HybridAgent on Environments.puzzlewithenemies.PuzzleWithEnemies ===

 A  S  .  .  . 
 .  .  T  T  . 
 T  .  .  .  . 
 E  .  D  E  . 
 .  .  .  .  . 

Score: 0, Door Open: False, Alive: True

Switch activated! Door is now open.
Collected a treasure!
Enemy moved onto agent! Game over.
Steps: 11, Score: 3
Path: [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 4), (2, 3), (3, 3)]
```