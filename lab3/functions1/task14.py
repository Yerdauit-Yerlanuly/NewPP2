from task1 import converttoounces
from task2 import converttof
from task3 import solve


x = int(input())
print(converttoounces(x))


x = int(input())
print(converttof(x))


numheads = int(input())
numlegs = int(input())
chickens, rabbits = solve(numheads, numlegs)
print(chickens," ", rabbits)