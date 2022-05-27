def getAllEdges(graph, INF):

    edgeArr = []

    if (len(graph) == 0):
        return edgeArr

    for i in range(len(graph)):
        for j in range(len(graph[len(graph) - 1])):
            if (graph[i][j] != INF):
                edgeArr.append([i, j, graph[i][j]])

    return edgeArr

def isEmpty(queue):

    if (len(queue) == 0):
        return True
    return False

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

def allSubsetEdges(edges, size, vertex_n, INF):

    subsetNum = 0
    solution = []
    posX = INF
    posY = INF
    min = -1

    while (subsetNum < pow(2, size)):

        subPoints = []
        cost = 0

        for i in range(size):
            if(subsetNum & (1 << i)):
                posX = edges[i][0]
                posY = edges[i][1]
                cost += edges[i][2]
                subPoints.append([posX, posY])

        if(True == feasibleSolution(subPoints, vertex_n)):
            if(min == -1):
                solution = subPoints
                min = cost
            elif (cost < min):
                solution = subPoints
                min = cost

        subsetNum += 1

    return [solution, min]  

def bruteforce_MST(graph, INF):
    
    allEdges = getAllEdges(graph, INF)
    solution = allSubsetEdges(allEdges, len(allEdges), len(graph), INF)
    
    return solution
    print("-----Graph-----")
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            print(graph[i][j], end = " ")
        print("\n", end = "")
    print("---------------")
    print("The edges of MST: {}, Cost: {}".format(solution[0], solution[1]))
    print("---------------")

"""INF = float('inf')
# 22
graph = [
    [INF, 15, 9, INF, 1],
    [15, INF, INF, 6, 18],
    [9, INF, INF, 23, 4],
    [INF, 6, 23, INF, 11],
    [1, 15, 4, 11, INF]]
bruteforce_MST(graph, INF)

# 16
graph = [[INF, 2, INF, 6, INF],
        [2, INF, 3, 8, 5],
        [INF, 3, INF, INF, 7],
        [6, 8, INF, INF, 9],
        [INF, 5, 7, 9, INF]]
bruteforce_MST(graph, INF)

# 6
graph = [
    [INF, 1, 2, 10],
    [1, INF, INF, 4],
    [2, INF, INF, 3],
    [10, 4, 3, INF]]
bruteforce_MST(graph, INF)

# 43
graph = [
    [INF, 2, INF, INF, INF, 14, 8],
    [2, INF, 19, INF, INF, 25, INF],
    [INF, 19, 9, 5, 17, INF, INF],
    [INF, INF, 9, INF, 1, INF, INF],
    [INF, INF, 5, 1, INF, 13, INF],
    [14, 25, 17, INF, 13, INF, 21],
    [8, INF, INF, INF, INF, 21, INF]]
    
bruteforce_MST(graph, INF)"""