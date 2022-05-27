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

def contains(solution, target):
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            if (solution[i][j] == target):
                return True
    return False

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
            

def crossOver(populations, maxSize, vehicleSize):

    newChildren = []

    idx = 0
    while (idx < len(populations)):
        
        lBound = 0
        uBound = 0
        coeff = maxSize * vehicleSize
        while (lBound >= uBound):
            uBound = randrange(coeff)
            lBound = randrange(coeff)

        P1_encodedGene = encodeGenotype(populations[idx], maxSize, vehicleSize)
        P2_encodedGene = encodeGenotype(populations[idx + 1], maxSize, vehicleSize)

        while (lBound < uBound):
            P1_encodedGene[lBound], P2_encodedGene[lBound] = P2_encodedGene[lBound], P1_encodedGene[lBound]
            lBound += 1

        P1_encodedGene = PMX_lastStep(P1_encodedGene, maxSize)
        P2_encodedGene = PMX_lastStep(P2_encodedGene, maxSize)

        newChildren.append(decodeGenotype(P1_encodedGene, maxSize))
        newChildren.append(decodeGenotype(P2_encodedGene, maxSize))
        idx += 2

    return newChildren

def isMutation():
    if (randrange(4) == 0):
        return True
    else:
        return False

def mutation(children):

    for i in range(len(children)):
        idx_1 = randrange(len(children[i]))
        idx_2 = randrange(len(children[i]))

        children[i][idx_1], children[i][idx_2] = children[i][idx_2], children[i][idx_1]
    
    return children

def natural_selection(graph, populations, new_children, populationSize):
    
    temp_newPopulation = []
    for i in range(populationSize):
        temp_newPopulation.append(populations[i])
        temp_newPopulation.append(new_children[i])
 
    for i in range((2*populationSize)-1):
        for j in range(0, (2*populationSize)-i-1):
            if (heuristicCost(graph, temp_newPopulation[j]) > heuristicCost(graph, temp_newPopulation[j + 1])):
                temp_newPopulation[j], temp_newPopulation[j + 1] = temp_newPopulation[j + 1], temp_newPopulation[j]

    newPopulation = []
    for i in range(populationSize):
        newPopulation.append(temp_newPopulation[i])

    return newPopulation

def VRP_Algorithm_GA(graph, vehicleSize):

    populationSize = 6
    generationSize = len(graph) * 50
    populations = []
    
    for i in range(populationSize):
        populations.append(randomConstruct(graph, vehicleSize))

    for generation in range(generationSize):
        optimaSolution_cost = heuristicCost(graph, populations[0])
        optimaSolution = populations[0].copy()

        for idx in range(1, populationSize):
            if (optimaSolution_cost > heuristicCost(graph, populations[idx])):
                optimaSolution_cost = heuristicCost(graph, populations[idx])
                optimaSolution = populations[idx].copy()

        if (generation == generationSize - 1):
            return optimaSolution

        new_children = crossOver(populations.copy(), len(graph), vehicleSize)
        if (isMutation()):
            new_children = mutation(new_children)

        populations = natural_selection(graph, populations, new_children, populationSize)

def init_graph(vertex):
    graph = [[INF] * vertex for _ in range(vertex)]
    
    for i in range(vertex):
        for j in range(i + 1, vertex):
            if ((i == 0 and j == 2) or (i == 2 and j == 0)):
                graph[i][j] = graph[j][i] = 0
            else:
                graph[i][j] = graph[j][i] = random.randint(5, 10)
    return graph

s = time.time()
vertexSize = 10
vehicles = 5
depositFromCosts = [random.randint(5, 10) for i in range(vertexSize)]
graph = [
    [INF, 3, 4, 5],
    [3, INF, 6, 5],
    [4, 6, INF, 7],
    [5, 5, 7, INF]
]
graph = init_graph(vertexSize)

sol = VRP_Algorithm_GA(graph, vehicles)
e = time.time()
print("Solution: " + str(sol) + ", Cost: " + str(heuristicCost(graph, sol)))
print(e - s)