# Input
```bash
python3 main.py
```

# Output of SAT run
```bash
hwsat 10 50 1000 0.2 5
```

```
        Inst     Solved:        Obj:        Res:      Flips:       Time:

uf150-082.cnf          10       0.000       1.700     322.300       0.028
uf150-022.cnf          10       0.000       1.400     480.500       0.023
uf150-02.cnf          10       0.000       2.800     603.800       0.064
uf150-012.cnf           9       0.200      12.800     742.000       0.318
uf150-032.cnf          10       0.000       4.600     621.600       0.109
uf150-052.cnf          10       0.000       3.900     540.900       0.090
uf150-062.cnf           9       0.400      20.700     690.400       0.524
uf150-072.cnf          10       0.000       7.700     410.300       0.181
uf150-092.cnf          10       0.000       5.800     621.400       0.137
uf150-042.cnf          10       0.000       8.500     542.800       0.204

Combined

 Average
 of All
 Instances         9.8       0.060       6.990     557.600       0.168
```

```
Running HSAT on uf150-081.cnf for 100 runs
  Completed 10/100 runs
  Completed 20/100 runs
  Completed 30/100 runs
  Completed 40/100 runs
  Completed 50/100 runs
  Completed 60/100 runs
  Completed 70/100 runs
  Completed 80/100 runs
  Completed 90/100 runs
  Completed 100/100 runs

Running HSAT on uf150-099.cnf for 100 runs
  Completed 10/100 runs
  Completed 20/100 runs
  Completed 30/100 runs
  Completed 40/100 runs
  Completed 50/100 runs
  Completed 60/100 runs
  Completed 70/100 runs
  Completed 80/100 runs
  Completed 90/100 runs
  Completed 100/100 runs

Running HWSAT on uf150-081.cnf for 100 runs
  Completed 10/100 runs
  Completed 20/100 runs
  Completed 30/100 runs
  Completed 40/100 runs
  Completed 50/100 runs
  Completed 60/100 runs
  Completed 70/100 runs
  Completed 80/100 runs
  Completed 90/100 runs
  Completed 100/100 runs

Running HWSAT on uf150-099.cnf for 100 runs
  Completed 10/100 runs
  Completed 20/100 runs
  Completed 30/100 runs
  Completed 40/100 runs
  Completed 50/100 runs
  Completed 60/100 runs
  Completed 70/100 runs
  Completed 80/100 runs
  Completed 90/100 runs
  Completed 100/100 runs


HSAT on uf150-081.cnf: 44 runs hit the flip limit of 1000.
HWSAT on uf150-081.cnf: 27 runs hit the flip limit of 1000.

Graph was generated and displayed:
```
![Runlength Distribution uf150-81](/Optimization/SATs/Figure_1.png)
```

HSAT on uf150-099.cnf: 2 runs hit the flip limit of 1000.
HWSAT on uf150-099.cnf: 1 runs hit the flip limit of 1000.

Graph was generated and displayed:
```

![Runlength Distribution uf150-99](/Optimization/SATs/Figure_2.png)

