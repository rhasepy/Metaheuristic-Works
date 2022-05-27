from random import randrange
import math

from PSO_Sort import updatePosition

# Check queue is empty or not
def isEmpty(queue):

    if (len(queue) == 0):
        return True
    return False

# Calculate and return cost of solution
def edgesCost(arr):

    cost = 0
    for i in range(len(arr)):
        cost += arr[i][2]

    return cost

# detect circle with breadth first search on choosen edges
def detectCircle(edges_arr):

    for i in range(len(edges_arr)):

        queue = []
        
        start = edges_arr[i][0]
        dest = edges_arr[i][1]
        queue.append([start, dest])

        while (False == isEmpty(queue)):
            point = queue.pop(0)
            pos_source = point[0]
            pos_dest = point[1]
 
            if (pos_dest == start):
                return True

            for j in range(len(edges_arr)):
                if(pos_dest == edges_arr[j][0]):
                    if (not ((edges_arr[j][1] == pos_source) & (edges_arr[j][0] == pos_dest))):
                        queue.append(edges_arr[j])

    return False

# Check and return true if the solution is feasible (not circle and contains all vertexes)
# Otherwise return false
def feasibleSolution(pointArr, vertex_n):

    # if the subset does not contain any edge it is not feasible
    if (len(pointArr) == 0):
        return False

    if (len(pointArr) < (vertex_n - 1)):
        return False

    # Check duplicate in solution space
    for i in range(len(pointArr)):
        
        dup_source = pointArr[i][0]
        dup_dest = pointArr[i][1]

        for j in range(len(pointArr)):
            if ((pointArr[j][0] == dup_dest) & (pointArr[j][1] == dup_source)):
                return False

    # fill the visited table
    visited = [False] * vertex_n
    for i in range(len(pointArr)):
        
        if (pointArr[i][2] == 0):
            return False

        posX = pointArr[i][0]
        posY = pointArr[i][1]
        visited[posX] = True
        visited[posY] = True

    # if did not visit all vertexes it is not feasible
    for i in range(len(visited)):
        if (False == visited[i]):
            return False

    # permutate and fill array with all point of visited edge
    # to detect circle
    permutatedPointArr = []
    for i in range(len(pointArr)):
        permutatedPointArr.append([pointArr[i][0], pointArr[i][1]])
        permutatedPointArr.append([pointArr[i][1], pointArr[i][0]])
    
    # detect circle
    return (not detectCircle(permutatedPointArr))

# Get ell edges as a array of arrays
def getAllEdges(graph, INF):

    edgeArr = []

    if (len(graph) == 0):
        return edgeArr
    
    for i in range(len(graph)):
        for j in range(len(graph[len(graph) - 1])):
            if (graph[i][j] != INF):
                edgeArr.append([i, j, graph[i][j]])

    return edgeArr

# the random construct the array
def randomConstruct(vertex, arr:list):

    returnArr = []
    rand_size = vertex - 1

    while (rand_size > 0):
        idx = randrange(len(arr))
        returnArr.append(arr[idx])
        arr.pop(idx)
        rand_size -= 1

    return returnArr

def returnMinimizedNeighboor(solution, grph, edgesCache):

    returnArr = []
    returnArrCpy = solution.copy()
    cost = edgesCost(solution)

    for i in range(len(solution)):
        for j in range(len(edgesCache)):
            temp = solution[i]
            solution[i] = edgesCache[j]

            if (True == feasibleSolution(solution, len(grph))):
                tempCost = edgesCost(solution)

                if (tempCost < cost):
                    cost = tempCost
                    returnArr.clear()
                    for idx in range(len(solution)):
                        returnArr.append(solution[idx])

            solution[i] = temp

    if (len(returnArr) == 0):
        return returnArrCpy

    return returnArr

def updatePosition(positionV, velocityV, cache, vertex):

    for i in range(len(positionV)):
        for idx in range(velocityV[i]):
            rand1 = randrange(len(positionV[i]))
            rand2 = randrange(len(cache))
            positionV[i][rand1], cache[rand2] = cache[rand2], positionV[i][rand1]
            while (False == feasibleSolution(positionV[i], vertex)):
                rand1 = randrange(len(positionV[i]))
                rand2 = randrange(len(cache))
                positionV[i][rand1], cache[rand2] = cache[rand2], positionV[i][rand1]

def PSO_Mst(graph, INF):

    edgesCache = getAllEdges(graph, INF)
    initialSolution = randomConstruct(len(graph), edgesCache)
    while (False == feasibleSolution(initialSolution, len(graph))):
        for i in range(len(initialSolution)):
            edgesCache.append(initialSolution[i])
        initialSolution = randomConstruct(len(graph), edgesCache)

    # particle size
    particle_size = len(graph)
    # particle swarm array
    pArr = []
    # iteration size
    iter_size = 200
    # pBest
    pBest = initialSolution.copy()
    # gBest
    gBest = initialSolution.copy()
    # velocity vector
    velocityVector = []
    # constant values
    c1 = 6
    c2 = 4
    # random values
    rand1 = randrange(3)
    rand2 = randrange(3)

    for i in range(particle_size):
        
        cache_temp = getAllEdges(graph, INF)
        temp = randomConstruct(len(graph), cache_temp)
        while (False == feasibleSolution(temp, len(graph))):
            for i in range(len(temp)):
                cache_temp.append(temp[i])
            temp = randomConstruct(len(graph), cache_temp)

        pArr.append(temp.copy())
        velocityVector.append(0)

    for i in range(iter_size):
        
        # update local best positions
        for iter in range(len(pArr)):
            if (edgesCost(pBest) > edgesCost(pArr[iter])):
                pBest = pArr[iter].copy()

            # v(i+1) = vi + ci * rand1 * (pbest - x)
            # + c2 * rand2 * (gbest - x)
            velocityVector[iter] += c1 * rand1 * (edgesCost(pBest) - edgesCost(pArr[iter])) 
            velocityVector[iter] += c2 * rand2 * (edgesCost(gBest) - edgesCost(pArr[iter]))

        # update global best positions
        if (edgesCost(pBest) < edgesCost(gBest)):
            gBest = pBest.copy()
        # move and update position
        updatePosition(pArr, velocityVector, edgesCache, len(graph))

    return gBest