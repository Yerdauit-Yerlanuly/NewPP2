def has_33(nums):
    for i in range(len(nums) - 2):
        if nums[i] == 0 and nums[i + 1] == 0 and nums[i+2] == 7:
            return True
    return False

str_numbers = input()
int_list = [int(x) for x in str_numbers.split()]
print(has_33(int_list))