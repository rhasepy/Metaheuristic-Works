import math
import random
from random import randrange

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

"""# Check and return true if the solution is feasible (not circle and contains all vertexes)
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
        posX = pointArr[i][0]
        posY = pointArr[i][1]
        visited[posX] = True
        visited[posY] = True

    # if did not visit all vertexes it is not feasible
    for i in range(len(visited)):
        if (False == visited[i]):
            return False
    
    return (len(pointArr) == (vertex_n -1))"""

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

# Cool down tempreture
def g(T, t):
    return T * 0.99

# SA Algorithm implementattion
def returnSimulatedAnnealingSolution(initSolution, grph, edgesCache):
    
    halt_criteria = True
    terminate_cond = True

    T = (0.3 * len(initSolution))  # Tempreture
    t = 0                 # Term count

    while (halt_criteria):

        iterator = 0
        terminate_cond = True
        while (terminate_cond):
            # get neighboorhood
            rand_idx = randrange(len(edgesCache))
            rand_jdx = randrange(len(initSolution))
            randVal_jdx = initSolution[rand_jdx]
            
            tempSolution = []
            for i in range(len(initSolution)):
                if (i == rand_jdx):
                    tempSolution.append(edgesCache[rand_idx])
                else:
                    tempSolution.append(initSolution[i])

            if (feasibleSolution(tempSolution, len(grph))):
                powerOfe = edgesCost(tempSolution) - edgesCost(initSolution)

                # Sometimes on the e^(Delta / T) occurs overflow exception
                # If the exception occur then algorithm goes to greedy 
                try:
                    if (edgesCost(initSolution) > edgesCost(tempSolution)):
                        edgesCache.pop(rand_idx)
                        edgesCache.append(randVal_jdx)
                        initSolution = tempSolution
                    elif ((random.random() < math.exp(powerOfe / T))):
                        edgesCache.pop(rand_idx)
                        edgesCache.append(randVal_jdx)
                        initSolution = tempSolution
                except:
                    dummyOp = 0
            else:
                continue
            
            if (iterator == len(initSolution)):
                terminate_cond = False
            else:
                iterator += 1
        
        T *= 0.99;
        t += 1
        if (t == 100):
            halt_criteria = False

    return initSolution

# Generate random solution from graph and run SA algorithm for optmization
def simulatedAnnealing_MST(graph, INF):

    allEdges = getAllEdges(graph, INF)
    initialSolution = randomConstruct(len(graph), allEdges)

    while (False == feasibleSolution(initialSolution, len(graph))):
        for i in range(len(initialSolution)):
            allEdges.append(initialSolution[i])
        initialSolution = randomConstruct(len(graph), allEdges)

    return returnSimulatedAnnealingSolution(initialSolution, graph, allEdges)

INF = float('-inf')