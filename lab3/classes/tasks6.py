def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

numbers_input = input()
numbers = list(map(int, numbers_input.split()))

prime_numbers = list(filter(lambda x: is_prime(x), numbers))

print(prime_numbers)
