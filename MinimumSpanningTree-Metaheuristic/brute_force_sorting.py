# This may be instead of objective function
def check_solution(arr):
    for idx in range(1, len(arr)):
        if(arr[idx] < arr[idx - 1]):
            return False
    return True

def copy_solution_array(arr):
    solArr = [0] * len(arr)
    for idx in range(len(arr)):
        solArr[idx] = arr[idx]
    
    return solArr

def permutation(arr, s_idx, permSize, solution:list):

    if (True == check_solution(arr)):
        solution.append(copy_solution_array(arr))
        return
    
    for idx in range(s_idx, permSize + 1):
        arr[s_idx], arr[idx] = arr[idx], arr[s_idx]
        permutation(arr, s_idx + 1, permSize, solution)
        arr[s_idx], arr[idx] = arr[idx], arr[s_idx]

def bruteforce(arr):
    solution = []
    permutation(arr, 0, len(arr) - 1, solution)

    if(len(solution) > 0):
        return solution[0]

    return []