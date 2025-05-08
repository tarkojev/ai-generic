#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module implements the GSAT and WalkSAT algorithms for solving
the Boolean satisfiability problem (SAT). The GSAT algorithm is a
local search algorithm that attempts to find a satisfying assignment
for a given Boolean formula in conjunctive normal form (CNF).
The WalkSAT algorithm is a stochastic local search algorithm that
combines random walks with greedy search to find a satisfying
assignment for a given Boolean formula in CNF.
The GSAT_solver class implements the GSAT and WalkSAT algorithms
and provides methods for reading SAT instances from files,
generating random solutions, flipping variables, updating counts,
selecting variables based on different heuristics, and checking
the validity of the solution.
The code also includes a main function that allows the user
to run the GSAT and WalkSAT algorithms on SAT instances
from a specified directory. The user can specify the algorithm,
the number of runs, the maximum number of restarts,
the maximum number of flips, the walk probability,
and the tabu tenure.
The module includes a function for generating run-length
distributions and plotting the results.
"""

import numpy as np
from time import perf_counter
import random
import sys
from os import listdir
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

random.seed(42)
np.random.seed(42)


'''
Data structures
state:          the current candidate solution
clauses:        list of lists, each list contains the literal of the clause
unsat_clauses:  the index of each currently unsat clause
makecounts:     the current makecount for each variable 
                (number of currently unsat clauses involving the variable) 
breakcounts:    the current breakcount for each variable 
                (number of currently sat clauses involving the variable, 
                 where the variable is the only satisfying literal of the clause
                 i.e the clause will go unsat if this variable is flipped) 
litToClauses:   dictionary containing 2*vars entries, one for each literal associated with each variable

NB: The variables and their associated literatls are numbered 1..n rather than 0..n-1, 
so to allow us to index in with variable number without having to -1 every time, 
a lot of the data structures are set up to be of size n+1, with the first element 
(index 0) ignored
'''

class GSAT_solver:
    
    def __init__(self, file, _h, _wp, _maxFlips, _maxRestarts, _tl):
        self.maxFlips = _maxFlips   # input: Number of flips before restarting
        self.maxRestarts = _maxRestarts     # input: Number of restarts before exiting
        self.flips = 0              # current number of flips performed
        self.restarts = 0           # current number of restarts performed
        self.nVars, self.nClauses, self.clauses, self.litToClauses = -1,-1,[],{}
        self.readInstance(file)
        self.state = [0 for _ in range(self.nVars+1)]
        self.makecounts = np.zeros(self.nVars+1,dtype=int) # unsat that would go sat
        self.breakcounts = np.zeros(self.nVars+1,dtype=int) # sat that would go unsat
        self.lastFlip = np.zeros(self.nVars+1,dtype=int) # unsat that would go sat
        self.bestSol = [0 for _ in range(self.nVars)]   # Current best solution found so far
        self.bestObj = self.nClauses+1          # Current best objective found so far (obj of bestSol)
        self.breakcounts[0] = self.nClauses+1 # sat that would go unsat
        self.wp = _wp   # input: walk probability
        self.h = _h     # input: heuristic to choose variable
        self.tl = _tl

    def readInstance(self, fName):
        file        = open(fName, 'r')
        current_clause = []
        clauseInd = 0
    
        for line in file:
            data = line.split()
    
            if len(data) == 0:
                continue
            if data[0] == 'c':
                continue
            if data[0] == 'p':
                self.nVars  = int(data[2])
                self.nClauses    = int(data[3])
                
                continue
            if data[0] == '%':
                break
            if self.nVars == -1 or self.nClauses == -1:
                print ("Error, unexpected data")
                sys.exit(0)
    
            # Now data represents a clause
            for var_i in data:
                literal = int(var_i)
                if literal == 0:
                    self.clauses.append(current_clause)
                    current_clause = []
                    clauseInd += 1
                    continue
                current_clause.append(literal)
                if literal in self.litToClauses:
                    self.litToClauses[literal].add(clauseInd)
                else:
                    self.litToClauses[literal] = set([clauseInd])
                    
        for i in range(1,self.nVars+1):
            if i not in self.litToClauses:
                self.litToClauses[i] = set()
            if -i not in self.litToClauses:
                self.litToClauses[-i] = set()
                    
        if self.nClauses != len(self.clauses):
            print(self.nClauses, len(self.clauses))
            print ("Unexpected number of clauses in the problem")
            sys.exit(0)
        file.close()

    def generateSolution(self):
        for i in range(1, self.nVars+1):
            choice = [-1,1]
            self.state[i] = (i * random.choice(choice))

    def initial_cost(self):
        # Compute objective value of initial solution, reset counters and recompute
        self.obj = self.nClauses
        self.unsat_clauses = set()
        self.makecounts = np.zeros(self.nVars+1,dtype=int) # unsat that would go sat
        self.breakcounts = np.zeros(self.nVars+1,dtype=int) # sat that would go unsat
        self.breakcounts[0] = self.nClauses+1
        num_unsat = 0
        clsInd = 0
        for clause in self.clauses:
            satLits = 0
            breakV = 0
            cStatus = False
            for lit in clause:
                if lit in self.state:
                    cStatus = True
                    satLits += 1
                    breakV = lit
                if satLits > 1:
                    break
            if satLits == 1:
                self.breakcounts[abs(breakV)] += 1
            if not cStatus:
                num_unsat += 1
                self.unsat_clauses.add(clsInd)
                for lit in clause:
                    self.makecounts[abs(lit)] += 1
            clsInd += 1
        self.obj = num_unsat
        if self.bestObj == -1:
            self.bestObj = num_unsat
            self.bestSol = self.state[1:]

    def flip(self, variable):
        self.flips += 1
        self.state[variable] *= -1
        self.update_counts(variable)
        self.lastFlip[variable] = self.flips

    # Function to update objective value and counts of variables 
    # Run after flipping 
    def update_counts(self, variable):
        literal = self.state[variable]
        for clauseInd in self.litToClauses[literal]:
            satLits = 0
            if clauseInd in self.unsat_clauses:
                for lit in self.clauses[clauseInd]:
                    self.makecounts[abs(lit)] -= 1
                # Was unsat so only flipvar now satisfies it 
                self.breakcounts[variable] += 1
            else:
                for lit in self.clauses[clauseInd]:
                    if lit in self.state:
                        satLits += 1
                        if lit != literal:
                            breaklit = lit
                if satLits == 2:
                    self.breakcounts[abs(breaklit)] -=1
        self.unsat_clauses = self.unsat_clauses - self.litToClauses[literal]
        self.obj = len(self.unsat_clauses)
        for clauseInd in self.litToClauses[literal*(-1)]:
            satLits = 0
            cStatus = False
            for lit in self.clauses[clauseInd]:
                if lit in self.state:
                    cStatus = True
                    satLits += 1
                    breaklit = lit
            if satLits == 1:
                self.breakcounts[abs(breaklit)] += 1
            if not cStatus:
                self.breakcounts[variable] -= 1 # flipvar was only 1 satisfying it
                self.obj += 1
                self.unsat_clauses.add(clauseInd)
                for lit in self.clauses[clauseInd]:
                    self.makecounts[abs(lit)] += 1

    def selectVar(self):
        if self.h =="gsat":
            return self.selectGSATvar()
        elif self.h == "gwsat":
            return self.selectGWSATvar()
        elif self.h == "gsatTabu":
            return self.selectGSATtabuvar()
        elif self.h == "hsat":
            return self.selectHSATvar()
        elif self.h == "hwsat":
            return self.selectHWSATvar()
        elif self.h == "walksat":
            return self.selectWalkSATvar()
        elif self.h == "walksatTabu":
            return self.selectWalkSATtabuvar()
        elif self.h == "customsat":
            return self.selectCustomSATvar()
        else:
            return self.selectCustomSATvar()

        
    def selectGWSATvar(self):
        if random.random() < self.wp:
            nextvar = self.selectRWvar()
        else:
            nextvar = self.selectGSATvar()
        return nextvar

    def selectHSATvar(self):
        gains = self.makecounts-self.breakcounts
        hvars = np.where( gains == np.amax(gains))[0]
        return hvars[np.where(self.lastFlip[hvars]== np.amin(self.lastFlip[hvars]))[0]][0]

    def selectHWSATvar(self):
        if random.random() < self.wp:
            nextvar = self.selectRWvar()
        else:
            nextvar = self.selectHSATvar()
        return nextvar
    
    def selectGSATvar(self):
        gains = self.makecounts-self.breakcounts
        hvars = np.where( gains == np.amax(gains))[0]
        return np.random.choice(hvars)
        
    def selectRWvar(self):
        hvars = np.where( self.makecounts > 0 )[0]
        return np.random.choice(hvars)

    def selectWalkSATvar(self):
        nextCls = random.choice(tuple(self.unsat_clauses))
        varsCls = [abs(lit) for lit in self.clauses[nextCls]]
        gains = np.array([self.breakcounts[i] for i in varsCls])
        hvars = np.where( gains == 0)[0]
        if len(hvars)>0:
            return varsCls[np.random.choice(hvars)]
        elif random.random() < self.wp:
            return random.choice(varsCls)
        else:
            hvars = np.where( gains == np.amin(gains))[0]
            return varsCls[np.random.choice(hvars)]

    def selectGSATtabuvar(self):
        '''
        Add tabu search to basic gsat, with aspiration criteria of 
        improving on best solution found so far in this search attempt 
        (i.e. not including from previous restarts).
        Advice: adapt Gsat code from selectGSATvar and add
        tabu criteria using LastFlip data structure
        '''
        gains = self.makecounts - self.breakcounts
        sorted_gains = np.unique(gains)
        sorted_gains.sort()  
        sorted_gains = sorted_gains[::-1] # Sort gains in desc order to prioritize variables with the highest gain first to flip

        # Iterate over gains 
        for gain in sorted_gains:
            hvars = np.where(gains == gain)[0]
            # Filter out tabu variables unless they meet the aspiration criterion
            non_tabu_vars = [
                var for var in hvars
                if (self.flips - self.lastFlip[var] >= self.tl) or # If the number of flips since var was last flipped is greater than or equal to the tabu tenure, then var is not tabu
                (self.obj - gains[var] < self.bestObj) # If flipping var results in fewer unsatisfied clauses than the best found so far in current search attempt, then  var flipping is allowed despite it being tabu, thus overrides it
            ]
            # If there are vars with asapiration criterion select randomly one of variables in non_tabu_vars to flip
            if non_tabu_vars:
                return np.random.choice(non_tabu_vars)
        # If no non-tabu variables found after checking all gains, select among tabu variables with highest gain   
        hvars = np.where(gains == sorted_gains[0])[0]
        last_flips = self.lastFlip[hvars]
        min_last_flip = np.min(last_flips)
        least_recent_vars = hvars[last_flips == min_last_flip]
        return np.random.choice(least_recent_vars)

    def selectCustomSATvar(self):
        '''
        (a) If promising variable, promising variable step 
            (select variable with largest net gain > 0,
                     if such variable exists)
        (b) Otherwise randomly choose unsat clause
            i. Random walk step with probability wp: 
                choose variable of clause at random
            ii. Otherwise choose variable with maximum net gain, 
                breaking ties by choosing the least recently flipped
        Advice: adapt WalkSAT code from selectWalkSATvar
        '''

        # (a): Check for hvars with net gain > 0
        gains = self.makecounts - self.breakcounts
        hvars = np.where(gains > 0)[0]
        # Greedily select a potential variable from hvars with highest net gain if it exists
        if len(hvars) > 0:
            max_gain = np.max(gains[hvars])
            max_gain_vars = hvars[gains[hvars] == max_gain]
            return np.random.choice(max_gain_vars)
        # (b): Randomly choose an unsatisfied clause
        else:
            # Select randomly unsatisfied clause
            nextCls = random.choice(tuple(self.unsat_clauses))
            varsCls = np.array([abs(lit) for lit in self.clauses[nextCls]])
            # Decide Between Random Walk or Greedy Step:
            if random.random() < self.wp: # Radnom walk step with probability wp: choose variable of clause at random to help escape local optima
                return np.random.choice(varsCls) 
            else: # Greedy Step with 1 - wp probability: choose variable of clause with maximum net gain
                gainCLs = gains[varsCls]
                max_gain = np.max(gainCLs)
                max_gain_vars = varsCls[gainCLs == max_gain]
                last_flips = self.lastFlip[max_gain_vars] # Break ties by choosing the least of recently flipped variable
                min_last_flip = np.min(last_flips)
                least_recent_vars = [var for var in max_gain_vars if self.lastFlip[var] == min_last_flip]
                return np.random.choice(least_recent_vars)

    def solve(self):
        self.restarts = 0
        while self.restarts < self.maxRestarts and self.bestObj > 0:
            self.restarts += 1
            self.generateSolution()
            self.initial_cost()
            self.flips = 0
            self.lastFlip = np.zeros(self.nVars+1,dtype=int) 
            self.bestObj = self.obj
            self.bestSol = self.state[1:].copy()
            while self.flips < self.maxFlips and self.bestObj > 0:
                nextvar = self.selectVar()
                self.flip(nextvar)
                if self.obj < self.bestObj:
                    self.bestObj = self.obj
                    self.bestSol = self.state[1:]

        if self.bestObj == 0:
            solutionChecker(self.clauses, self.bestSol)
        return self.flips, self.restarts, self.bestObj

def solutionChecker(clauses, sol):
    unsat_clause = 0
    for clause in clauses:
        cStatus = False
        for var in clause:
            if var in sol:
                cStatus = True
                break
        if not cStatus:
            unsat_clause+=1
    if unsat_clause > 0:
        print ("UNSAT Clauses: ",unsat_clause)
        return False
    return True



def main():
    if len(sys.argv) == 1: 
        filesDir = "uf150-645" 
        alg, nRuns, maxRes, maxFlips, wp, tl, sNum = "hwsat", 10, 50, 1000, 0.2, 5, 3
    elif len(sys.argv) < 9:
        print(len(sys.argv))
        print ("Error - Incorrect input")
        print ("Expecting python gsat.py [fileDir] [alg] [number of runs] [max restarts]",
               "[max flips] [walk prob] [studentNum]")
        sys.exit(0)
    else:
        _, filesDir, alg, nRuns, maxRes, maxFlips, wp, tl, sNum  = sys.argv
        sNum, nRuns, maxRes, maxFlips, wp, tl = int(sNum), int(nRuns), int(maxRes), int(maxFlips), float(wp), int(tl)

    solved_list = []
    obj_list = []
    res_list = []
    flips_list = []
    time_list = []

    # Iterate through all instances in the directory that end with 
    # last value of your student number 
    statsList = ["Inst", "Solved:", "Obj:","Res:", "Flips:","Time:"]
    h_format_row = "{:>12}"*len(statsList) 
    d_format_row = "{:>12}{:>12}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}"  # changed format as it was not suitable during tests
    print(alg, nRuns, maxRes, maxFlips, wp, tl) # just in the end realised 'tl' was not added, but its not critical, just cosmetics
    print(h_format_row.format(*statsList))
    for filename in listdir(filesDir):
        if filename.endswith("2.cnf"): # SN ends with 2
            satInst=filesDir+"/"+filename
            avgRestarts, avgFlips, avgUnsatC, avgTime, unsolved = 0, 0, 0, 0, 0

            for i in range(nRuns):
                random.seed(260382 +sNum + i*100)
                np.random.seed(260382 + sNum + i*100)
                gsat = GSAT_solver(satInst, alg, wp, maxFlips, maxRes, tl) # Default parameters
                startPython = perf_counter()
                ctrFlips, ctrRestarts, ctrObj = gsat.solve()
                stopPython = perf_counter()
                avgFlips += ctrFlips
                avgRestarts += ctrRestarts
                avgUnsatC += ctrObj
                avgTime += (stopPython-startPython)
                if ctrObj > 0:
                    unsolved += 1
            resList = [filename, nRuns - unsolved, avgUnsatC/nRuns, avgRestarts/nRuns, avgFlips/nRuns, avgTime/nRuns]
            print(d_format_row.format(*resList))

            # Appending for average results
            solved_list.append(nRuns - unsolved)
            obj_list.append(avgUnsatC / nRuns)
            res_list.append(avgRestarts / nRuns)
            flips_list.append(avgFlips / nRuns)
            time_list.append(avgTime / nRuns)

    # Give average results accross all isntances
    if solved_list:  # Check if the list is not empty
        avg_solved = np.mean(solved_list)
        avg_obj = np.mean(obj_list)
        avg_res = np.mean(res_list)
        avg_flips = np.mean(flips_list)
        avg_time = np.mean(time_list)
        avg_resList = ["Combined\n Average\n of All\n Instances", round(avg_solved, 2), round(avg_obj, 2), round(avg_res, 2), round(avg_flips, 2), round(avg_time, 3)]
        print(d_format_row.format(*avg_resList))

    # Runlength distribution
    t_inst = ["uf150-081.cnf", "uf150-099.cnf"]
    a_alg = ["hsat", "hwsat"]
    nruns = 100
    r_res = {alg: {inst: [] for inst in t_inst} for alg in a_alg}
    for alg in a_alg:
        for inst in t_inst:
            satInst = f"{filesDir}/{inst}"
            print(f"\nRunning {alg.upper()} on {inst} for {nruns} runs")
            for run in range(nruns):
                random.seed(260382 + sNum + run * 100)
                np.random.seed(260382 + sNum + run * 100)
                gsat = GSAT_solver(satInst, alg, wp, maxFlips, maxRes, tl)
                ctrFlips, ctrRestarts, ctrObj = gsat.solve()
                r_res[alg][inst].append(ctrFlips) # Record number of flips
                # Printin progress every 10 runs
                if (run + 1) % 10 == 0:
                    print(f"  Completed {run + 1}/{nruns} runs")

    # Plotting the runlength distrubituon results
    for inst in t_inst:
        plt.figure(figsize=(10, 6))
        for alg in a_alg:
            flips = r_res[alg][inst] # Get list of flip counts
            # Check if any run hits the flip limit
            flip_limit_hits = sum(1 for f in flips if f == maxFlips)
            print(f"{alg.upper()} on {inst}: {flip_limit_hits} runs hit the flip limit of {maxFlips}.")
            flips.sort() # Asc
            k = len(flips) # Total flips
            rt_j = flips # Sorted list of flip counts from mulpiple runs
            # j divide by total
            j_over_k = [j / k for j in range(1, k + 1)] # Total probabilities for each number of Flips
            plt.plot(rt_j, j_over_k, label=alg.upper(), marker='o')
        plt.title(f"Runlength Distribution Plot for {inst}")
        plt.xlabel("Flips (rt_j)")
        plt.ylabel("Solve Probability (j/k)")
        plt.legend(title="Heuristic")
        plt.tight_layout()
        plt.grid(True)
        plt.show()
        with warnings.catch_warnings(record=True) as caught_warnings: # adding warning handler as my system doesn't display the image for some reason so I have to save it locally
            warnings.simplefilter("always")
            plt.show()
            if any(isinstance(w.message, UserWarning) for w in caught_warnings):
                plt.savefig(f"runlength_distribution{inst}.png")
                print(f"\nWarning: The graph plot could not be displayed interactively. Instead, it has been saved locally in your current directory as 'runlength_distribution{inst}.png'.")
            else:
                print("\nGraph was generated and displayed.\n")

main ()