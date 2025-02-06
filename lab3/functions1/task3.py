def solve(numheads, numlegs):
    x = (4 * numheads - numlegs) / 2
    y = numheads - x
    
    if x >= 0 and y >= 0:
        return int(x), int(y)
    else:
        return "No valid solution"