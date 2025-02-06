import itertools

def string_permutations(s):
    return [''.join(p) for p in itertools.permutations(s)]

s = input()
print(string_permutations(s))