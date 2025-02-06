def unique_elements(list):
    unique_list = []
    for item in list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

x = input()
list = [int(i) for i in x]
print(unique_elements(list))