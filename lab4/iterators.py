# 1. Generator for squares of numbers up to N
def squares(n):
    for i in range(n + 1):
        yield i * i

# 2. Generator for even numbers up to n
def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i

# 3. Generator for numbers divisible by 3 and 4 up to n
def div_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

# 4. Generator for squares between a and b
def squares_range(a, b):
    for i in range(a, b + 1):
        yield i * i

# 5. Generator that returns numbers from n down to 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

print(list(squares(10)))
print(list(even_numbers(10)))
print(list(div_by_3_and_4(50)))
print(list(squares_range(3, 7)))
print(list(countdown(10)))