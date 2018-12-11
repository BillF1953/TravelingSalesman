#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 17:31:38 2018

@author: anani
"""

import numpy as np
import pickle



def evaluate_cost(solution,adj):#sum the edges in the given solution
    total = 0
    for i in range(len(adj)-1):
        total += adj[solution[i],solution[i+1]]
    return total

def getNeighbor(solution):
    # retrieve the neighborhood of a solution
    # A neighbor is defined as the same solution but with two cities swapped
    n1 = np.random.randint(len(solution))
    n2 = np.random.randint(len(solution))
    solution2 = np.array(solution, copy=True) 
    f = solution2[n1]
    
    solution2[n1] = solution2[n2]
    solution2[n2] = f
    
    return solution2
    
def check_if_Tabu(solution,TabuList):
    # check if a given solution exists in the tabu list
    for visitedSolution in TabuList:
        if (visitedSolution == solution).all():
            return True
    return False
    

def solve(adj,city):
    
    csv_data = open(city + ".csv",'w')
    csv_data.write('Iteration, Cost' + '\n')
    nodes = np.arange(adj.shape[0])
    random_solution = np.random.permutation(nodes) 
    shortMemorySize = 1000
    numberOfNeighbors = 1000
    bestSolution = random_solution
    bestCandidateSolution = random_solution
    
    
    TabuList = [] # short memory list of visited solutions
    TabuList.append(random_solution)
    
    
    print("Initial Cost: ", evaluate_cost(bestSolution,adj))
    i = 0
    
    maximumIterations = 50000
    
    pastCost = evaluate_cost(bestSolution,adj)
    csv_data.write(str(i) + ',' + str(pastCost) + '\n')
    k = 0
    while(i < maximumIterations):
        
        for j in range(numberOfNeighbors):
             neighborSolution = getNeighbor(bestSolution) # neighbors of current best solution
             neighborSolutionCost = evaluate_cost(neighborSolution,adj)
             bestCandidateSolutionCost = evaluate_cost(bestCandidateSolution,adj)
             if (not check_if_Tabu(neighborSolution,TabuList)) and neighborSolutionCost < bestCandidateSolutionCost:
                 bestCandidateSolution = neighborSolution
               
        
        
        if evaluate_cost(bestCandidateSolution,adj) <  evaluate_cost(bestSolution,adj):
            bestSolution = bestCandidateSolution
            currentCost = evaluate_cost(bestSolution,adj)
        
        TabuList.append(bestCandidateSolution)
        
        if len(TabuList) <= shortMemorySize :
            TabuList.pop()
            
        i += 1
        csv_data.write(str(i) + ',' + str(currentCost) + '\n')
        if currentCost == pastCost:
            
            k += 1 # increment the number of consecutive iterations without improvement
            if k == 5: #if no improvement over the last five iterations, terminate search
                print(i)
                break
        else: # reset k: the counter of consecutive iterations without improvement
            k=0
        
        pastCost = evaluate_cost(bestSolution,adj)
         
    print("Final Cost: ", evaluate_cost(bestSolution,adj))
    
    
    csv_data.close()
    return bestSolution

if __name__ == "__main__":
    
    
    cities = ['djibouti','qatar','luxembourg']
    for city in cities:
        print(city)
        with open('data/{}.p'.format(city), 'rb') as f:
            adj = pickle.load(f)
        solve(adj,city)
            
