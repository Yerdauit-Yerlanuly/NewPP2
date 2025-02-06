# Create a List:

thislist = ["abc", 34, True, 40, "male"]
print(thislist)

# Print the number of items in the list:

print(len(thislist))

# Data type of list
print(type(thislist))

# Access elements 
print(thislist[1])
print(thislist[1:3])

# Change the second value by replacing it with two new values:
thislist[1:2] = ["blackcurrant", "watermelon"]
print(thislist)

# The insert() method inserts an item at the specified index:

thislist = ["apple", "banana", "cherry"]
thislist.insert(2, "watermelon")

# Using the append() method to append an item:

thislist = ["apple", "banana", "cherry"]
thislist.append("orange")

# Remove "banana":

thislist = ["apple", "banana", "cherry"]
thislist.remove("banana")

#Remove the first item:

thislist = ["apple", "banana", "cherry"]
del thislist[0]

# loop list
thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)

for i in range(len(thislist)):
  print(thislist[i])

# list comprehension
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = [x for x in fruits if "a" in x]
print(newlist)

# Sort the list alphabetically:
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort()

# Sort in descending order
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort(reverse = True)

# Join lists
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

list3 = list1 + list2
print(list3)

