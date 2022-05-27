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

# Generate random solution from graph and run SA algorithm for optmization
def simulatedAnnealingSorting(arr):

    currentArr = randomConstruct(arr)

    halt_criteria = True
    terminate_cond = True

    T = (0.3) * len(currentArr)
    t = 0

    while (halt_criteria):

        iterator = 0
        terminate_cond = True
        while (terminate_cond):
            
            if (arrayCost(currentArr) == 0):
                return currentArr

            tempArr = []
            rand_idx = randrange(len(currentArr))
            rand_jdx = randrange(len(currentArr))
            
            for i in range(len(currentArr)):
                tempArr.append(currentArr[i])
            
            # Get neighboor two element swapped each other, this is my neighboord design
            tempArr[rand_idx], tempArr[rand_jdx] = tempArr[rand_jdx], tempArr[rand_idx]
            powerOfe = arrayCost(tempArr) - arrayCost(currentArr)

            # Sometimes on the e^(delta/T) occurs overflow exception
            # # If the exception occur then algorithm goes to greedy 
            try:
                if (arrayCost(currentArr) > arrayCost(tempArr)):
                    currentArr = tempArr
                elif ((random.random() < math.exp(powerOfe / T))):
                    currentArr = tempArr
            except:
                dummyOp = 0
            
            if (iterator == len(currentArr)):
                terminate_cond = False
            else:
                iterator += 1
        
        T *= 0.99
        t += 1
        if (t == 100):
            halt_criteria = False
    
    return currentArr