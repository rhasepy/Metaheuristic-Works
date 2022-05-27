def backtracking(arr, visitTable, solution):

    interrupt_subproblems = False
    
    for idx in range(len(arr)):

        # base cases for interrupt algorithm
        if (True == interrupt_subproblems):
            break
        if (True == visitTable[idx]):
            continue
        if ((idx > 0) & (arr[idx] == arr[idx - 1]) & (False == visitTable[idx - 1])):
            continue
        
        # if the choosen decision variable is not feasible break the loop
        # this is may be instead of objective function
        if(len(solution) > 0):
            if(solution[len(solution) - 1] > arr[idx]):
                interrupt_subproblems = True
                continue

        # idx of table is visited for check base cases
        visitTable[idx] = True
        
        # append the feasible decision varible in the solution vector
        solution.append(arr[idx])
        # recursive call for back-tracking
        backtracking(arr, visitTable, solution)

        # if the solution is feasible so all decision varible true sequences
        # then return this solution
        if(len(solution) == len(arr)):
            return

        # idx of table is not visited
        visitTable[idx] = False

        # if the solution is not feasile remove last added decision variable
        del solution[-1] 

def backtracking_sort(arr):
    visitTable = [False] * len(arr)
    solution = []
    backtracking(arr, visitTable, solution)
    return solution