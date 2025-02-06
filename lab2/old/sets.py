#Iterating through set
thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x)

#Add an item to a set, using the add() method:

thisset = {"apple", "banana", "cherry"}
thisset.add("orange")

tropical = {"pineapple", "mango", "papaya"}
thisset.update(tropical)

# Remove a random item by using the pop() method:

thisset = {"apple", "banana", "cherry"}

x = thisset.pop()

# Loop sets
thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x)