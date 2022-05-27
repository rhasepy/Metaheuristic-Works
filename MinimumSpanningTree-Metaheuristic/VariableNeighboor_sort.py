import random
from random import randrange

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

# Shake operation 
def shaking(arr, level):

    arr_ = []
    for i in range(len(arr)):
        arr_.append(arr[i])

    swappedArr = []
    while (len(swappedArr) < (2*level)):
        rand_i = randrange(len(arr))
        rand_j = rand_i
        while (rand_i == rand_j):
            rand_j = randrange(len(arr))

        if (not ((swappedArr.__contains__(rand_i)) & (swappedArr.__contains__(rand_j)))):
            arr_[rand_i], arr_[rand_j] = arr_[rand_i], arr_[rand_j]
            swappedArr.append(rand_i)
            swappedArr.append(rand_j)

    return arr_

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

def VNS_Sort(arr):

    newArr = randomConstruct(arr)
    lMax = (len(newArr) / 2)    # max level

    for level in range(int(lMax)):
        
        # Shaking operation
        stochasticSolution = shaking(newArr, level)

        # Local Search
        deterministicSolution = localSearch_Sorting(stochasticSolution)

        if (arrayCost(stochasticSolution) > arrayCost(deterministicSolution)):
            newArr = deterministicSolution
            level = 0

    return newArr