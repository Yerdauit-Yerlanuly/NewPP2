def is_polindrom(str):
    str1 = ''.join(reversed(str))
    if str1 == str:
        return 'is polindrom'
    else:
        return 'is not polindrom'
    
x = input()
print(is_polindrom(x))