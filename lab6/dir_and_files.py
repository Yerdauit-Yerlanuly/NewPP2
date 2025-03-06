import os
from pathlib import Path


# Task 1
def list_only_dirs(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def list_only_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def list_all_dirs_files(path):
    return os.listdir(path)

path = input("Enter the path: ")
if not os.path.exists(path):
    print("Invalid path!")
else:
    print("Directories:", list_only_dirs(path))
    print("Files:", list_only_files(path))
    print("All Directories and Files:", list_all_dirs_files(path))


# Task 2
def check_existence(path):
    return os.path.exists(path)

def check_readability(path):
    try:
        with open(path, "r") as f:
            return f.readable()
    except IOError:
        return False 

def check_writability(path):
    try:
        with open(path, "a") as f:
            return f.writable()
    except IOError:
        return False 

path = input("Enter the path: ")
print(check_existence(path))
print(check_readability(path))
print(check_writability(path))


# Task 3
def test_path(path):
    if os.path.exists(path):
        print(f"The path '{path}' exists.")

        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        
        print(f"Directory: {directory}")
        print(f"Filename: {filename}")
    else:
        print(f"The path '{path}' does not exist.")

path = input("Enter the path to test: ")
test_path(path)

# Task 4
def count_lines(file):
    count = 0
    try:
        with open(file, "r") as f:
            for i in f:
                count += 1
        return count        
    except IOError:
        return False 
    

path = input("Enter the path: ")
print(count_lines(path))


# Task 5
def write_list_to_file(file, list):
    try:
        with open(file, "w") as f:
            for item in list:
                f.write(f"{item}\n")  
        print(f"List has been written to '{file}' successfully.")
    except IOError:
        print("Error")


data = ["Sushi", "Pizza", "Doner"]  
file_path = input("Enter the path: ")

write_list_to_file(file_path, data)

# Task 6
def generate_26_files():
    for letter in range(65, 91):  
        filename = f"{chr(letter)}.txt"
        with open(filename, "w") as f:
            if os.path.exists(filename):
                os.remove(filename)
    print("26 text files (A.txt to Z.txt) have been created.")

generate_26_files()


# Task 7
def copy_file_contents(source, destination):
    if not os.path.exists(source):
        print("Source file does not exist.")
    
    with open(source, "r") as src, open(destination, "w") as dest:
        dest.write(src.read())
    print(f"Contents of {source} have been copied to {destination}.")

path1 = input("Enter the source: ")
path2 = input("Enter the destination: ")
copy_file_contents(path1, path2)


# Task 8
def del_file(file):
    if check_existence(file) and check_readability(file) and check_writability(file):
        try:
            os.remove(file)
            print(f"Success: The file '{file}' has been deleted.")
        except IOError:
            print("Error")
    else:
        print("Impossible to delete the file.")

path = input("Enter the path: ")
del_file(path)
