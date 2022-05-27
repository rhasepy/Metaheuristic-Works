import math
import random
from random import randrange

# the random construct the array
def randomConstruct(arr:list):

    returnArr = []

    while (len(arr) > 0):
        idx = randrange(len(arr))
        returnArr.append(arr[idx])
        arr.pop(idx)

    return returnArr

# calculating the cost, if he is looking at those behind him, 
# they must be bigger, if he is looking ahead, he must be smaller than them
def arrayCost(arr):

    count = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            if((i < j) & (arr[j] < arr[i])):
                count += 1
            elif((i > j) & (arr[i] < arr[j])):
                count += 1

    return count

def contains(arr, item):
    for i in range(len(arr)):
        if arr[i] == item:
            return True
    return False

# my cross over operator function
# this take parents and first-last matching
# for example 
# parent 0 - parent len(array) match
# parent 1 - parent len(array) -1 
# i use 2 point crossover algorithm
# i try 1 point and n point
#  but 2 point it is good for me because less complexity and give good solution to me
def crossover_operation(parent_arr, population_size, elementSize):
    
    newChildren = []

    j = population_size - 1
    for i in range(int(population_size / 2)):

        lowBound = randrange(elementSize)
        upBound = randrange(elementSize)
        if (lowBound > upBound):
            lowBound, upBound = upBound, lowBound
        idx = 0 + lowBound
        bound = 0 + upBound

        newChild_1 = [0]*elementSize
        newChild_2 = [0]*elementSize

        while (idx <= bound):
            newChild_1[idx] = parent_arr[i][idx]
            newChild_2[idx] = parent_arr[j][idx]
            idx += 1
        
        idx = 0
        idx_ = 0
        bound = elementSize
        while ((idx < elementSize) and (idx_ < elementSize)):
            if (idx == (lowBound)):
                idx = upBound + 1
            else:
                if (not contains(newChild_1, parent_arr[j][idx_])):
                    newChild_1[idx] = parent_arr[j][idx_]
                    idx += 1
                idx_ += 1

        idx = 0
        idx_ = 0
        bound = elementSize
        while ((idx < elementSize) and (idx_ < elementSize)):
            if (idx == (lowBound)):
                idx = upBound + 1
            else:
                if (not contains(newChild_2, parent_arr[i][idx_])):
                    newChild_2[idx] = parent_arr[i][idx_]
                    idx += 1
                idx_ += 1

        newChildren.append(newChild_1)
        newChildren.append(newChild_2)
        j -= 1
        
    return newChildren

# natural selection function
# if the solution is good solution survive
# but it is bad solution dead!
def natural_selection(parent_arr, children_arr, population_size):
    
    temp_newPopulation = []
    for i in range(population_size):
        temp_newPopulation.append(parent_arr[i])
        temp_newPopulation.append(children_arr[i])
 
    for i in range((2*population_size)-1):
        for j in range(0, (2*population_size)-i-1):
            if (arrayCost(temp_newPopulation[j]) > arrayCost(temp_newPopulation[j + 1])):
                temp_newPopulation[j], temp_newPopulation[j + 1] = temp_newPopulation[j + 1], temp_newPopulation[j]

    newPopulation = []
    for i in range(population_size):
        newPopulation.append(temp_newPopulation[i])

    return newPopulation

# using swap mutation technique
def mutation(children_arr):
    for i in range(len(children_arr)):
        rand_i = randrange(len(children_arr[i]))
        rand_idx = randrange(len(children_arr[i]))
        children_arr[i][rand_i], children_arr[i][rand_idx] = children_arr[i][rand_idx], children_arr[i][rand_i]
    
    return children_arr

def isMutation():
    if (randrange(4) == 0):
        return True
    else:
        return False

def geneticSort(arr):

    # if there is any duplicate array element it is not necesarry and im ignore it
    newTemp = []
    for i in range(len(arr)):
        if (not contains(newTemp, arr[i])):
            newTemp.append(arr[i])
    arr = newTemp

    population = []
    population_size = 6
    generation_size = len(arr) * 50

    for i in range(0, population_size):
        temp = arr.copy()
        population.append(randomConstruct(temp))

    for generation in range(generation_size):
        optimaSolution_cost = arrayCost(population[0])
        optimaSolution = population[0].copy()

        for idx in range(1, population_size):
            if (optimaSolution_cost > arrayCost(population[idx])):
                optimaSolution_cost = arrayCost(population[idx])
                optimaSolution = population[idx].copy()

        # if the cost is zero for any elements of population return it because it is global optimal
        # i know it is global and i'm using for complexity optimization
        if (optimaSolution_cost == 0):
            return optimaSolution

        # if the step is last generation return best solution
        if (generation == (generation_size - 1)):
            return optimaSolution

        # cross-over and produce new children
        new_children = crossover_operation(population, population_size, len(arr))

        # if is there mutation probablity then mutate it
        # mutattion has 25% rate
        if (isMutation()):
            new_children = mutation(new_children)

        # new population contains children and parents, and then comes natural selection 
        # the most low cost 6th element survive and new population contains just these
        population = natural_selection(population, new_children, population_size)

    # if generation size is 0 then return arr because there will be not any changes solution
    return arr