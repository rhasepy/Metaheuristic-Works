from random import randrange

# the random construct the array
def randomConstruct(arr:list):

    returnArr = []

    while (len(arr) > 0):
        idx = randrange(len(arr))
        returnArr.append(arr[idx])
        arr.pop(idx)

    return returnArr

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

# local search untill find minimized solution
def localSearch_Sorting(arr):

    newArr = randomConstruct(arr)

    while (True):
        
        cost = arrayCost(newArr)
        newArr = returnMinimizedNeighboor(newArr)
        tempArr = []

        for i in range(len(newArr)):
            tempArr.append(newArr[i])

        if (cost < arrayCost(newArr)):
            return tempArr

        if (arrayCost(newArr) == 0):
            return newArr