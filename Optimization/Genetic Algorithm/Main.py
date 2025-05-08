#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analysis of TSP using Genetic Algorithm
"""

import random
from TSP_Individual import *
import sys
import numpy as np
from scipy.spatial import distance_matrix
import pandas as pd 
import time
myStudentNum = 42
random.seed(myStudentNum)

def readInstance(fName):
    file = open(fName, 'r')
    size = int(file.readline())
    inst = {}
    for i in range(size):
        line=file.readline()
        (myid, x, y) = line.split()
        inst[int(myid)] = (int(x), int(y))
    file.close()
    return inst

def genDists(fName):
    file = open(fName, 'r')
    size = int(file.readline())
    instance = {}
    for i in range(size):
        line=file.readline()
        (myid, x, y) = line.split()
        instance[int(myid)] = (int(x), int(y))
    file.close()
    dfcity= pd.DataFrame.from_dict(instance, orient="index")
    dfcity.rename(columns ={0:"x",1:"y"}, inplace = True)
    flt_dists = distance_matrix(dfcity.values,dfcity.values)
    return (np.rint(flt_dists)).astype(int)

class BasicTSP:
    
    # modified
    def __init__(self, _fName, _maxIterations, _popSize, _initH, _xoverProb, _mutationRate, _elites, _trunk, _dists):
        """
        Parameters and general variables
        Note not all parameters are currently used, it is up to you to implement how you wish to use them and where
        """

        self.population     = []
        self.matingPool     = []
        self.best           = None
        self.popSize        = int(_popSize)
        self.genSize        = None
        self.initH        = int(_initH)
        self.crossoverProb  = float(_xoverProb)
        self.mutationRate   = float(_mutationRate)
        self.maxIterations  = int(_maxIterations)
        self.fName          = _fName
        self.iteration      = 0
        self.data           = {}
        self.elites        = round(self.popSize * float(_elites))
        self.trunkSize = round(self.popSize * float(_trunk))
        self.dists           = _dists

        self.readInstance()
        self.bestInitSol = self.initPopulation()

        # ensuring population size is even
        if self.popSize % 2 != 0:
            self.popSize += 1

    def readInstance(self):
        """
        Reading an instance from fName
        """
        file = open(self.fName, 'r')
        self.genSize = int(file.readline())
        self.data = {}
        for line in file:
            (cid, x, y) = line.split()
            self.data[int(cid)] = (int(x), int(y))
        file.close()

    def initPopulation(self):
        """
        Creating individuals in the initial population
        Either pure random tours (initH=0), or with insertion heuristic (initH=1)
        """
        for i in range(0, self.popSize):
            individual = Individual(self.genSize, self.data,self.initH, self.dists, [])
            if not(self.initH):
                individual.computeFitness()
            self.population.append(individual)

        self.best = self.population[0].copy()
        for ind_i in self.population:
            if self.best.getFitness() > ind_i.getFitness():
                self.best = ind_i.copy()
        return self.best.getFitness()

    def updateBest(self, candidate):
        if self.best == None or candidate.getFitness() < self.best.getFitness():
            self.best = candidate.copy()
    
    def randomSelection(self):
        """
        Random (uniform) selection of two individuals
        """
        indA = self.matingPool[ random.randint(0, self.trunkSize-1) ]
        indB = self.matingPool[ random.randint(0, self.trunkSize-1) ]
        return [indA, indB]
    
    # modified
    def crossover(self, indA, indB):
        """
        Executes an order1 crossover and returns the genes for a new individual
        """
        
        # broke down on child1 and child2 and modified class parameters to copy parent genes
        if random.random() > self.crossoverProb:
            child1 = Individual(self.genSize, self.data, 0, self.dists, indA.genes.copy()) # just copying parent A genes
            child2 = Individual(self.genSize, self.data, 0, self.dists, indB.genes.copy()) # copy parent B genes
            return child1, child2
        
        midP=random.randint(1, self.genSize-2)
        
        # child 1 crossover
        c1p1 =  indA.genes[0:midP] # getting parent A genes
        c1genes = c1p1 + [i for i in indB.genes if i not in c1p1] # mixing remaining genes from parent B
        child1 = Individual(self.genSize, self.data, 0,self.dists, c1genes) # child with new mixed genes from both parents 
        
        # child 2 crossover
        c2p1 =  indB.genes[0:midP] # getting parent B genes
        c2genes = c2p1 + [i for i in indA.genes if i not in c2p1] # mixing remaining genes from parent A
        child2 = Individual(self.genSize, self.data, 0,self.dists, c2genes) # same as child1
        
        return child1, child2
    
    def mutation(self, ind):
        """
        Mutate an individual by swapping two cities with certain probability (i.e., mutation rate)
        This mutator performs recipricol exchange
        """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp

    # modified matingPool 
    def updateMatingPool(self):
        """
        Updating the mating pool before creating a new generation.
        Uses truncation selection
        Note we are only storing the gene values and fitness of every 
        chromosome in prev pop
        """
        mybest = self.population[0:self.trunkSize]
        best_fits = [i.getFitness() for i in mybest]
        worst_fit=max(best_fits)
        worst_idx = best_fits.index(worst_fit)
        for i in range(self.trunkSize,self.popSize):
            if self.population[i].getFitness() < worst_fit:
                mybest[worst_idx] = self.population[i]
                best_fits[worst_idx] = self.population[i].getFitness()
                worst_fit = max(best_fits)
                worst_idx = best_fits.index(worst_fit)
        self.matingPool = mybest[:] # creating separate individual objects for genes data due to indX.genes attribute
                
        ## Add truncation to mating pool, separately store elite best
        if self.elites < self.trunkSize:
            x = self.elites
        else:
            x = self.trunkSize
        elite_sols = mybest[0:x]
        if x:
            elite_fits = [i.getFitness() for i in elite_sols]
            worst_fit = max(elite_fits)
            worst_idx = elite_fits.index(worst_fit)
            for i in range(x,len(mybest)):
                if mybest[i].getFitness() < worst_fit:
                    elite_sols[worst_idx] = mybest[i]
                    elite_fits[worst_idx] = mybest[i].getFitness()
                    worst_fit = max(elite_fits)
                    worst_idx = elite_fits.index(worst_fit)
        return elite_sols

    # modified to create new generation for 2 children
    def newGeneration(self):
        """
        Creating a new generation
        1. Selection
        2. Crossover (2 childeren)
        3. Mutation
        """
        for i in range(self.elites, self.popSize, 2):
            [ind1, ind2] = self.randomSelection() # select from mating pool
            child1, child2 = self.crossover(ind1, ind2)
            self.mutation(child1)
            self.mutation(child2)
            child1.computeFitness()
            child2.computeFitness()
            self.updateBest(child1)
            self.updateBest(child2)
            self.population[i] = child1
            # safecheck ensuring population index for odd numbers
            if (i + 1) < self.popSize:
                self.population[i + 1] = child2 

    def GAStep(self):
        """
        One step in the GA main algorithm
        1. Updating mating pool with current population
        2. Creating a new Generation
        """

        elite_sols = self.updateMatingPool()
        # print()
        self.population[:self.elites] = elite_sols
        self.newGeneration()

    def search(self):
        """
        General search template.
        Iterates for a given number of steps
        """
        self.iteration = 0
        while self.iteration < self.maxIterations:
            self.GAStep()
            self.iteration += 1

        return self.best.getFitness(), self.bestInitSol, self.best.genes

# new function
def GA_solution_checker(tour_solution, distance, reported_fitness):
    # check if cities are occuring exactly once or not missing, otherwise its not a valid permutation
    num_city = distance.shape[0] # correspinding number of cities
    city_id = set(range(1, num_city + 1)) # set suquence of city IDs
    city = set(tour_solution) # checks if cities are duplicated or missing
    if city != city_id:
        return False, False, None # returns False for both is_valid(def main) and is_valid_fitness and None for total_tour_distance

    # Compute the total distance
    total_tour_distance = 0
    for i in range(len(tour_solution)):
        from_city = tour_solution[i] - 1
        to_city = tour_solution[(i + 1) % len(tour_solution)] - 1 # ensuring that after last city it wrap around to the first city
        total_tour_distance += distance[from_city, to_city] # total distance is summed distances per each from current city to next city
    valid_fitness = (total_tour_distance == reported_fitness)
    return True, valid_fitness, total_tour_distance

def main():
    if len(sys.argv) < 9:
        print ("Error - Incorrect input")
        print ("Expecting python TSP.py [instance] [number of runs] [number of iterations] [population size]", 
                "[initialisation method] [xover prob] [mutate prob] [elitism] [truncation] [student number]")
        sys.exit(0)
    '''
    Reading in parameters, but it is up to you to implement what needs implementing
    TO DO:
    1/ Adapt to produce 2 children from each crossover - done
    2/ Add solution checker of final GA solution in each run to verify it is correct - done
    3/ Add code for metrics - done
    '''
    _, inst, nRuns, nIters, pop, initH, pC, pM, el, tr = sys.argv
    d = genDists(inst)
    nRuns = int(nRuns)
    random.seed(myStudentNum)
    startTime = round(time.time(),4) # added metrics: calculate time for initial run
    ga = BasicTSP(inst, nIters, pop, initH, pC, pM, el, tr, d)
    bestDist, distInit, bestSol = ga.search()
    avgDist, avgInitDist = bestDist, distInit
    stopTime = time.time()
    execution_time = stopTime - startTime
    total_distances = [bestDist] # added metrics: total distance
    total_runtimes = [execution_time]
    print(f"Current Run: 1")
    print(f"Run 1: Tour Distance/Fitness: {bestDist}")
    print(f"Run 1: Execution time of the Run: {execution_time:.2f} seconds")
    print(f"Run 1: Tour Path: {bestSol}")
    
    for i in range(1,nRuns):
        print(f"Current Run: {i + 1}")
        startTime = round(time.time(),4) # added metrics: calculate time per each run
        random.seed(myStudentNum+i*100)
        ga = BasicTSP(inst, nIters, pop, initH, pC, pM, el, tr, d)
        dist, distInit, sol = ga.search()
        stopTime = round(time.time(),4)
        execution_time = stopTime - startTime 
        total_runtimes.append(execution_time)
        total_distances.append(dist)
        avgDist += dist
        avgInitDist += distInit
        avg_run_distance = (distInit + dist) / 2 # metrics
        print(f"Average Distance/Fitness for current run: {avg_run_distance:.2f}")
        avg_run_distance = avgDist / (i + 1) # metrics
        print(f"Average Distance/Fitness after {i + 1} runs: {avg_run_distance:.2f}")
        # added GA solution verification/error handling
        # sol - best tour sequence, d - distance, dist - reported fitness value
        is_valid, is_valid_fitness, is_total_tour_distance = GA_solution_checker(sol, d, dist) 
        if not is_valid: # if the tour does not include all cities exactly once
            print(f"Run {i + 1}: Invalid solution.")
        elif not is_valid_fitness: # if the total_tour_distance and reported_fitness are not matching
            print(f"Run {i + 1}: Fitness mismatch! Reported distance: {dist}, Total Tour Distance: {is_total_tour_distance}")
        
    # some other metrics output
        if dist < bestDist:
            bestDist = dist
            bestSol = sol
        print(f"Run {i + 1}: Tour Distance/Fitness: {bestDist}")
        print(f"Run {i + 1}: Tour Path: {sol}")
        print(f"Run {i + 1}: Execution time of the Run: {execution_time:.2f} seconds")
    
    print(f"\nYay all {nRuns} Runs are now completed! Here is the summary of all GA Runs:\n")
    avg_distance = avgDist / nRuns
    total_time = sum(total_runtimes)
    print(f"Average Distance/Fitness over {nRuns} runs: {avg_distance}")
    print(f"Total time of all Runs: {total_time:.2f} seconds")
    print(f"Best Overall Distance/Fitness: {bestDist}")
    print(f"Best Overall Tour: {bestSol}")
    
main()

# default run parameters: python3 TSP_student.py inst-a.tsp 10 1000 100 0 0.9 0.2 0.1 0.5
