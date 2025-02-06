import random

def guess_num(num, name):
    x = random.randint(1,20)
    guesscount = 0
    while num != x:
        if num < x:
            print('Your guess is too low.')
            print('Take a guess')
        if num > x:
            print('Your guess in too high.')
            print('Take a guess')
        num = int(input())
        guesscount += 1
    return print('Good job,', name,'! You guessed my number in', guesscount, 'guesses!')


print("hello, what's your name?")
i = str(input())
x = int(input())
guess_num(x,i)