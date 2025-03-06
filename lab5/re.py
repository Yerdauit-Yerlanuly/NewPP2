import re

def match_a_b():
    pattern = r"ab*"
    i = input()
    print("Match found!" if re.fullmatch(pattern, i) else "No match.")

def match_a_bb():
    pattern = r"ab{2,3}"
    i = input()
    print("Match found!" if re.fullmatch(pattern, i) else "No match.")

def find_lowercase_underscore():
    pattern = r"[a-z]+_[a-z]+"
    i = input()
    print("Matches:", re.findall(pattern, i) or "No match.")

def find_upper_lower():
    pattern = r"[A-Z][a-z]+"
    i = input()
    print("Matches:", re.findall(pattern, i) or "No match.")

def match_a_anything_b():
    pattern = r"a.*b$"
    i = input()
    print("Match found!" if re.fullmatch(pattern, i) else "No match.")

def replace_delimiters():
    i = input()
    print("Modified string:", re.sub(r"[ ,.]", ":", i))

def snake_to_camel():
    i = input()
    print("CamelCase string:", re.sub(r'_([a-z])', lambda x: x.group(1).upper(), i))

def split_at_uppercase():
    i = input()
    print("Splitted words:", re.split(r"(?=[A-Z])", i))

def insert_spaces():
    i = input()
    print("Formatted string:", re.sub(r"([a-z])([A-Z])", r"\1 \2", i))

def camel_to_snake():
    i = input()
    print("Snake_case string:", re.sub(r"([a-z])([A-Z])", r"\1_\2", i).lower())

def main():
    print("Choose an option:")
    print("Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.")
    print("Write a Python program that matches a string that has an 'a' followed by two to three 'b'.")
    print("Write a Python program to find sequences of lowercase letters joined with a underscore.")
    print("Write a Python program to find the sequences of one upper case letter followed by lower case letters.")
    print("Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.")
    print("Write a Python program to replace all occurrences of space, comma, or dot with a colon.")
    print("Write a python program to convert snake case string to camel case string.")
    print("Write a Python program to split a string at uppercase letters.")
    print("Write a Python program to insert spaces between words starting with capital letters.")
    print("Write a Python program to convert a given camel case string to snake case.")

    choice = input()

    options = {
        "1": match_a_b,
        "2": match_a_bb,
        "3": find_lowercase_underscore,
        "4": find_upper_lower,
        "5": match_a_anything_b,
        "6": replace_delimiters,
        "7": snake_to_camel,
        "8": split_at_uppercase,
        "9": insert_spaces,
        "10": camel_to_snake
    }

    options[choice]()


if __name__ == "__main__":
    main()
