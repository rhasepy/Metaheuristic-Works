from random import randrange
import random
import time

INF = float("inf")

def isFeasible(graph, solutionVehicles, vertexSize):

    if (heuristicCost(graph, solutionVehicles) == INF):
        return False

    visitedTable = {}
    for i in range(vertexSize):
        visitedTable[i] = 0

    for i in range(len(solutionVehicles)):
        for j in solutionVehicles[i]:
            visitedTable[j] += 1

    for i in range(vertexSize):
        if (visitedTable[i] != 1):
            return False
    return True

def heuristicCost(graph, solutionVehicles):
    
    global depositFromCosts
    heuristicCost = 0

    for i in range(len(solutionVehicles)):
        for j in range(len(solutionVehicles[i])):

            if (j == 0):
                heuristicCost += depositFromCosts[solutionVehicles[i][j]]
            if (j == len(solutionVehicles[i]) - 1):
                break
                
            heuristicCost += graph[solutionVehicles[i][j]][solutionVehicles[i][j + 1]]

    return heuristicCost 

def randomConstruct(graph, vehicleSize):

    while (True):
        vehicles = []
        for i in range(vehicleSize):
            vehicles.append([])

        for i in range(len(graph)):
            whichVehicle = randrange(vehicleSize)
            whichVertex = randrange(len(graph))

            vehicles[whichVehicle].append(whichVertex)
        
        if (isFeasible(graph, vehicles, len(graph))):
            return vehicles

def encodeGenotype(solution, maxSize, vehicleSize):
    
    encodedGeno = ""
    for i in range(maxSize):
        for j in range(vehicleSize):
            encodedGeno += '0'
    encodedGeno = list(encodedGeno)

    for i in range(len(solution)):
        for j in range(len(solution[i])):
            encodedGeno[(i * (maxSize)) + solution[i][j]] = '1'

    return encodedGeno

def decodeGenotype(encodedGenes, maxSize):

    decodedGeno = []
    subGeno = []
    for i in range(len(encodedGenes)):

        if (i % maxSize == 0 and i != 0):
            decodedGeno.append(subGeno.copy())
            subGeno = []

        if (encodedGenes[i] == '1'):
            subGeno.append(i % maxSize)
    
    decodedGeno.append(subGeno.copy())
    return decodedGeno

def shaking(solution, level, vehicleSize, graph):
    
    arr = encodeGenotype(solution, len(graph), vehicleSize)
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

    return decodeGenotype(arr_, len(graph))

def returnMinimizedNeighboor(arr, graph):

    cost = heuristicCost(graph, decodeGenotype(arr, len(graph)))
    nbArr = []

    for i in range(len(arr)):
        for j in  range(i+1, len(arr)):

            arr[i], arr[j] = arr[j], arr[i]
            
            if (isFeasible(graph, decodeGenotype(arr, len(graph)), len(graph))):
                tempCost = heuristicCost(graph, decodeGenotype(arr, len(graph)))
                if (cost > tempCost):
                    cost = tempCost
                    nbArr.clear()
                    for idx in range(0, len(arr)):
                        nbArr.append(arr[idx])

            arr[i], arr[j] = arr[j], arr[i]
    
    if (len(nbArr) == 0):
        return arr
    return nbArr

def localSearch(solution, vertexSize, vehicleSize, graph):

    newArr = encodeGenotype(solution.copy(), vertexSize, vehicleSize)

    while (True):
        
        currentArr = decodeGenotype(newArr, len(graph))

        newArr = returnMinimizedNeighboor(newArr, graph)

        current_cost = heuristicCost(graph, currentArr)
        new_cost = heuristicCost(graph, decodeGenotype(newArr, len(graph)))

        if (current_cost <= new_cost):
            return currentArr

def contains(solution, target):
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            if (solution[i][j] == target):
                return True
    return False

def PMX_lastStep(encodedGene, vertexSize):
    
    visited = []
    for i in range(vertexSize):
        visited.append(1)

    for i in range(len(encodedGene)):
        if (encodedGene[i] == '1'):

            idx = i % vertexSize
            
            if (visited[idx] == 1):
                visited[idx] = 0
            elif (visited[idx] == 0):
                encodedGene[i] = '0'

    for i in range(len(visited)):
        if (visited[i] == 1):
            for j in range(len(encodedGene)):
                if (j % vertexSize == i and visited[i] == 1):
                    if (encodedGene[j] == '0'):
                        encodedGene[j] = '1'
                        visited[i] = 0

    return encodedGene

def VRP_Algorithm_VNS(graph, vehicleSize):

    initial_solution = randomConstruct(graph, vehicleSize)
    lMax = (len(initial_solution) / 2)

    for level in range(int(lMax)):

        stochasticSolution = shaking(initial_solution, level, vehicleSize, graph)

        deterministicSoltuion = localSearch(initial_solution, len(graph), vehicleSize, graph)

        if (heuristicCost(graph, stochasticSolution) > heuristicCost(graph, deterministicSoltuion)):
            initial_solution = deterministicSoltuion
            level = 0
    
    return initial_solution

def init_graph(vertex):
    graph = [[INF] * vertex for _ in range(vertex)]
    
    for i in range(vertex):
        for j in range(i + 1, vertex):
            if ((i == 0 and j == 2) or (i == 2 and j == 0)):
                graph[i][j] = graph[j][i] = 0
            else:
                graph[i][j] = graph[j][i] = random.randint(5, 10)
    return graph


vertexSize = 10
vehicles = 5
depositFromCosts = [random.randint(5, 10) for i in range(vertexSize)]

graph = [
    [INF, 3, 4, 5],
    [3, INF, 6, 5],
    [4, 6, INF, 7],
    [5, 5, 7, INF]]

graph = init_graph(vertexSize)

sol = VRP_Algorithm_VNS(graph, vehicles)
print("Solution: " + str(sol) + ", Cost: " + str(heuristicCost(graph, sol)))