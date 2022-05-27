import random
from random import randrange
import math

from TabuMST import indexOf

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

# find neighboor and return minimized their cost
# neighboor is array that swapped 2 element each other
# so one element swap other one element
def returnMinimizedNeighboor(arr):

    cost = arrayCost(arr)
    nbArr = []

    for i in range(len(arr)):
        for j in  range(i+1, len(arr)):
            arr[i], arr[j] = arr[j], arr[i]
            
            tempCost = arrayCost(arr)
            if (cost > tempCost):
                cost = tempCost
                nbArr.clear()
                for idx in range(0, len(arr)):
                    nbArr.append(arr[idx])

            arr[i], arr[j] = arr[j], arr[i]
    
    return nbArr

def returnCandidateList(arr):
    nbArr = []

    for i in range(len(arr)):
        for j in  range(i+1, len(arr)):
            arr[i], arr[j] = arr[j], arr[i]
            nbArr.append(arr.copy())
            arr[i], arr[j] = arr[j], arr[i]
    
    return nbArr

# local search untill find minimized solution
def localSearch_Sorting(arr):

    #newArr = randomConstruct(arr.copy())
    newArr = arr.copy()
    while (True):
        
        currentArr = []

        for i in range(len(newArr)):
            currentArr.append(newArr[i])

        newArr = returnMinimizedNeighboor(newArr)
        cost = arrayCost(currentArr)

        if (cost < arrayCost(newArr)):
            return currentArr

        if (arrayCost(newArr) == 0):
            return newArr


# the random construct the array
def randomConstruct(arr:list):

    returnArr = []

    while (len(arr) > 0):
        idx = randrange(len(arr))
        returnArr.append(arr[idx])
        arr.pop(idx)

    return returnArr

# array contains element or not
def contains(arr, elem):
    
    for i in range(arr):
        if (arr[i] == elem):
            return True
    return False

def getNeighbor(arr):

    neighborSolution = []
    rand_idx = randrange(len(arr))
    rand_jdx = randrange(len(arr))
    
    for i in range(len(arr)):
        neighborSolution.append(arr[i])
    
    # Get neighboor two element swapped each other, this is my neighboord design
    neighborSolution[rand_idx], neighborSolution[rand_jdx] = neighborSolution[rand_jdx], neighborSolution[rand_idx]

    return neighborSolution

def equalSolutions(arr, arr_):
    for i in range(len(arr)):
        if (arr[i] != arr_[i]):
            return False
    return True

def searchTabuList(tabuList, target_solution):
    for i in range(len(tabuList)):
        if (equalSolutions(tabuList[i], target_solution)):
            return True
    return False

def isEqualArr(arr1, arr2):
    
    if (len(arr1) != len(arr2)):
        return False

    for i in range(len(arr1)):
        if (arr1[i] != arr2[i]):
            return False

    return True

def indexOf(cdList, arr):
    idx = 0
    for array in cdList:
        if (isEqualArr(arr, array)):
            return idx
        idx += 1
    return -1

def tabuSort(arr):
    
    # initial solution
    currentSolution = randomConstruct(arr)

    iter_size = 100
    tabu_tenure = int(math.sqrt(len(arr)))
    tabu_list = {}

    bestSolution = currentSolution

    for i in range(iter_size):
        
        # Candidate List
        cdList = returnCandidateList(currentSolution.copy())
        # new Solution
        newSolution = []

        # (candidate list - tabulist) + aspiration
        for item in tabu_list:
            idx = indexOf(cdList, item)
            if (idx != -1):
                # Aspiration
                if (arrayCost(currentSolution) < arrayCost(item)):
                    cdList.pop(idx)

        # new Solution = best New Set
        if (len(cdList) > 0):
            newSolution = cdList[0].copy()
            for item in cdList:
                if (arrayCost(newSolution) > arrayCost(item)):
                    newSolution = item.copy()

        # if the improve solution i keep in the variable this
        # if the last solution may be bad then apply local search it 
        # but i will not apply local search just tabu search
        if (arrayCost(currentSolution) > arrayCost(newSolution)):
            bestSolution = newSolution.copy()

        # update solution
        currentSolution = newSolution.copy()

        for sol in list(tabu_list):
            tabu_list[sol] -= 1
            if (tabu_list[sol] == 0):
                del tabu_list[sol]
        tabu_list[str(newSolution)] = tabu_tenure
    
    return bestSolution