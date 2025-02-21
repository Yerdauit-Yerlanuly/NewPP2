import math

# 1. Convert degree to radian
def degree_to_radian(degree):
    return math.radians(degree)

# 2. Area of a trapezoid
def trapezoid_area(height, base1, base2):
    return (base1 + base2) * height / 2

# 3. Area of a regular polygon
def regular_polygon_area(sides, side_length):
    return (sides * side_length**2) / (4 * math.tan(math.pi / sides))

# 4. Area of a parallelogram
def parallelogram_area(base, height):
    return base * height

print(degree_to_radian(15))
print(trapezoid_area(5, 5, 6))
print(regular_polygon_area(4, 25))
print(parallelogram_area(5, 6))