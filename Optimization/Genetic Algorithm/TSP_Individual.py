#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the Individual class for the TSP problem.
The Individual class represents a solution to the TSP problem, which is a
combinatorial optimization problem that aims to find the shortest possible route
that visits a set of cities and returns to the origin city.
The class includes methods for initializing the individual, computing its fitness,
and performing crossover and mutation operations.
The individual is represented as a list of genes, where each gene represents a city.
The fitness of the individual is calculated based on the distances between the cities
in the tour.
The class also includes a method for generating an initial solution using a greedy heuristic.
The insertion heuristic is used to generate an initial solution by iteratively
adding the nearest unvisited city to the tour.
"""

import random
import math


class Individual:
    def __init__(self, _size, _data, _initH, _d, cgenes):
        """
        Parameters and general variables
        """
        self.fitness    = 0
        self.genes      = []
        self.genSize    = _size
        self.data       = _data
        self.init       = _initH
        self.dists      = _d

        if cgenes: # Child genes from crossover
            self.genes = cgenes
        else:   # Random initialisation of genes
            if self.init:
                self.genes, self.fitness = self.insertion_heuristic1()
            else:
                self.genes = list(self.data.keys())
                random.shuffle(self.genes)

    def copy(self):
        """
        Creating a copy of an individual
        """
        ind = Individual(self.genSize, self.data, 0,self.dists, self.genes[0:self.genSize])
        ind.fitness = self.getFitness()
        return ind

    def getFitness(self):
        return self.fitness

    def computeFitness(self):
        """
        Computing the cost or fitness of the individual
        """
        self.fitness    = self.dists[self.genes[0]-1, self.genes[len(self.genes)-1]-1]
        for i in range(0, self.genSize-1):
            self.fitness += self.dists[self.genes[i]-1, self.genes[i+1]-1]

    def insertion_heuristic1(self):
        unvisited = list(self.data.keys())
        tCost = 0

        # Randomly choose a city to start the tour
        cIndex = random.randint(0, len(self.data)-1)
        tour = [unvisited[cIndex]] #Initialise tour to this city
        del unvisited[cIndex] # Remove from unvisited
        current_city = tour[0] # This variable will store the last city added to the tour in each iteration

        while len(unvisited) > 0:
            # initialise the distance (bcost) to first unvisited city
            bCity = unvisited[0]
            bCost = self.dists[current_city-1, bCity-1]
            bIndex = 0
            #Then iterate through remaining unvisited cities to see if there is a nearer city
            for city_index in range(1, len(unvisited)):
                city = unvisited[city_index]
                cost = self.dists[current_city-1, city-1]

                if bCost > cost:
                    bCost = cost
                    bIndex = city_index
            tCost += bCost                          # Update tour cost
            current_city = unvisited[bIndex]        # Update current city to new city chosen
            tour.append(current_city)
            del unvisited[bIndex]

        # Add distance from ginal city back to first city    
        tCost += self.dists[tour[-1]-1, tour[0]-1]
        
        return tour, tCost
