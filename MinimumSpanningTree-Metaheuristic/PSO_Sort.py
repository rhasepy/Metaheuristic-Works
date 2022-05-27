from random import randrange
import math

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

# Each particles moves velocity times 1 iteration
def updatePosition(positionV, velocityV):

    for i in range(len(positionV)):
        for idx in range(velocityV[i]):
            rand1 = randrange(len(positionV[i]))
            rand2 = randrange(len(positionV[i]))
            positionV[i][rand1], positionV[i][rand2] = positionV[i][rand2], positionV[i][rand1]

def PSOSort(arr):

    # particle size
    particle_size = len(arr)
    # particle swarm array
    pArr = []
    # iteration size
    iter_size = 200
    # pBest
    pBest = []
    # gBest
    gBest = randomConstruct(arr.copy())
    # velocity vector
    velocityVector = []
    # constant values
    c1 = 6
    c2 = 4
    # random values
    rand1 = randrange(3)
    rand2 = randrange(3)

    # initiliaze particles
    for i in range(particle_size):
        pArr.append(randomConstruct(arr.copy()))
        velocityVector.append(0)

    pBest = pArr[0].copy()

    # main loop
    for i in range(iter_size):

        # Calculate fitness function value each partitions
        for iter in range(len(pArr)):
            
            # update local best positions
            if ((arrayCost(pBest) > arrayCost(pArr[iter])) or (len(pBest) == 0)):
                pBest = pArr[iter].copy()

            # sorting problem specific case
            if (arrayCost(gBest) == 0):
                return gBest

            # v(i+1) = vi + ci * rand1 * (pbest - x)
            # + c2 * rand2 * (gbest - x)
            velocityVector[iter] += c1 * rand1 * (arrayCost(pBest) - arrayCost(pArr[iter])) 
            velocityVector[iter] += c2 * rand2 * (arrayCost(gBest) - arrayCost(pArr[iter]))
        
        # update global best positions
        if (arrayCost(pBest) < arrayCost(gBest)):
            gBest = pBest.copy()
        # move and update position
        updatePosition(pArr, velocityVector)

    return gBest