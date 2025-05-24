# Input
```bash
python3 bayesiannetwork.py
```

# Output of GA Run
```
Bayesian Network start.

Conditional Probability Tables:

Node: SE
P(SE | High) = 0.6
P(SE | Low) = 0.4

Node: PI
P(PI | Stable) = 0.7
P(PI | Unstable) = 0.3

Node: CP
P(CP | Stable, Strict) = 0.8
P(CP | Stable, Average) = 0.2
P(CP | Unstable, Strict) = 0.3
P(CP | Unstable, Average) = 0.7

Node: CEA
P(CEA | High, Strict, High) = 0.85
P(CEA | High, Strict, Low) = 0.15
P(CEA | High, Average, High) = 0.6
P(CEA | High, Average, Low) = 0.4
P(CEA | Low, Strict, High) = 0.5
P(CEA | Low, Strict, Low) = 0.5
P(CEA | Low, Average, High) = 0.2
P(CEA | Low, Average, Low) = 0.8

Node: CE
P(CE | High, Strict, Low) = 0.9
P(CE | Low, Strict, High) = 0.7
P(CE | High, Average, Low) = 0.3
P(CE | Low, Average, High) = 0.2

Query: P(CE=Low | SE=High, PI=Stable)

D-separation: PI and CE are independent given CP.
D-separation: SE and CE are independent given CEA.
P(CE=Low | SE=High, PI=Stable) = 0.720

Graph was generated and displayed.
```
![BNN](/Reasoning/Probabilistic%20Graphical%20Reasoning/Figure_bn.png)

```
 Bayesian Network end.
========================================
```