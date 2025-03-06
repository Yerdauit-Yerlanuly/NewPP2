import math
import time

# Task 1
def multiply_list(numbers):
    return math.prod(numbers)

nums = [2, 3, 4, 5]
result = multiply_list(nums)
print("Product of the list:", result)


# Task 2
def count_case(s):
    upper_count = sum(1 for char in s if char.isupper())
    lower_count = sum(1 for char in s if char.islower())
    return upper_count, lower_count

text = "Hello World!"
upper, lower = count_case(text)
print("Uppercase letters:", upper)
print("Lowercase letters:", lower)


# Task 3
def is_palindrome(s):
    return s == s[::-1]  

text = "madam"
if is_palindrome(text):
    print(f'"{text}" is a palindrome')
else:
    print(f'"{text}" is not a palindrome')


# Task 4
def delayed_sqrt(number, delay_ms):
    time.sleep(delay_ms / 1000)  
    result = math.sqrt(number)
    print(f"Square root of {number} after {delay_ms} milliseconds is {result}")

num = 25100
delay = 2123
delayed_sqrt(num, delay)


# Task 5
def all_true(tup):
    return all(tup)

t1 = (True, True, True)
t2 = (True, False, True)

print(all_true(t1))  
print(all_true(t2))