def greedy_algorithm_sorting(arr):

    solution = [0] * len(arr)
    sol_idx = 0
    
    for idx in (range(len(arr))):
        min_idx = idx

        for idx_ in range(idx + 1, len(arr)):
            # find minimum element every cycle and
            if(arr[min_idx] > arr[idx_]):
                min_idx = idx_

        # put the left of offset cause of approcah greedy next step
        solution[sol_idx] = arr[min_idx]
        arr[min_idx] = arr[idx]
        arr[idx] = solution[sol_idx]
        sol_idx += 1
        
    return solution