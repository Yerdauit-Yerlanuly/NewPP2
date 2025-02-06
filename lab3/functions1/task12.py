def histogram(num):
    for i in num:
        print("*" * i)

x = input().split()
numbers = [int(i) for i in x]
histogram(numbers)