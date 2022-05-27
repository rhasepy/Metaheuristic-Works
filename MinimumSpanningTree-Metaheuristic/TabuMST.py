from random import randrange
import math

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

def returnCandidateList(solution, grph, edgesCache):
    returnArr = []
    returnArrCpy = solution.copy()
    sol_cpy = solution.copy()

    for i in range(len(solution)):
        for j in range(len(edgesCache)):

            temp = sol_cpy[i]
            sol_cpy[i] = edgesCache[j]

            if (True == feasibleSolution(sol_cpy, len(grph))):
                returnArr.append(sol_cpy.copy())

            sol_cpy[i] = temp

    if (len(returnArr) == 0):
        return returnArrCpy

    return returnArr

def isEqualEdge(e1, e2):
    if (e1[0] == e2[0] and e1[1] == e2[1]):
        return True
    if (e1[0] == e2[1] and e1[1] == e2[0]):
        return True
    if (e1[1] == e2[0] and e1[0] == e2[1]):
        return True
    if (e1[1] == e2[1] and e1[0] == e2[2]):
        return True
    
    return False

def indexOf(edgeList, edge):
    
    idx = 0
    for e in edgeList:
        if (isEqualEdge(e, edge)):
           return idx
        idx += 1
    return -1
                

def tabuMST(graph, INF):

    allEdges = getAllEdges(graph, INF)
    initialSolution = randomConstruct(len(graph), allEdges)
    
    while (False == feasibleSolution(initialSolution, len(graph))):
        for i in range(len(initialSolution)):
            allEdges.append(initialSolution[i])
        initialSolution = randomConstruct(len(graph), allEdges)

    iter_size = 100
    tabu_tenure = int(math.sqrt(len(graph)))
    tabu_list = {}

    bestSolution = initialSolution.copy()
    
    for i in range(iter_size):

        # Candidate list
        cdList = returnCandidateList(initialSolution, graph, allEdges)
        # new solution
        newSolution = []

        # (candidate list - tablu list) + aspiration
        for item in tabu_list:
            idx = indexOf(cdList, item)
            if (idx != -1):
                # Aspiration
                if (edgesCost(item) > edgesCost(initialSolution)):
                    cdList.pop(idx)

        # new Solution = best New Set
        if (len(cdList) > 0):
            newSolution = cdList[0].copy()
            for item in cdList:
                if(edgesCost(newSolution) > edgesCost(item)):
                    newSolution = item.copy()

        # if the improve solution i keep in the variable this
        # if the last solution may be bad then apply local search it 
        # but i will not apply local search just tabu search
        if (edgesCost(initialSolution) > edgesCost(newSolution)):
            if (True == feasibleSolution(newSolution, len(graph))):
                bestSolution = newSolution.copy()

        # update solution
        initialSolution = newSolution.copy()

        # update tabu list
        for sol in list(tabu_list):
            tabu_list[sol] -= 1
            if (tabu_list[sol] == 0):
                del tabu_list[sol]
        tabu_list[str(newSolution)] = tabu_tenure
        
    return bestSolution