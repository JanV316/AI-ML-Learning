# variables.py
# Python Basics: Variables, Dynamic Typing, and Formatting
# ---------------------------------------------------------
# Explanation:
# A variable in Python is a named location in memory used to store data.
# Python uses dynamic typing, meaning you do not need to declare data types explicitly.
# Variable names should follow snake_case convention (e.g., student_name, age_in_years).

print("=" * 60)
print("PART 1: Variable Declaration & Dynamic Typing")
print("=" * 60)

# Creating variables of different types
student_name = "Alice"     # String (str)
age = 22                   # Integer (int)
gpa = 3.85                 # Floating point (float)
is_enrolled = True         # Boolean (bool)

print("Student Name:", student_name, "| Type:", type(student_name))
print("Age         :", age, "         | Type:", type(age))
print("GPA         :", gpa, "      | Type:", type(gpa))
print("Is Enrolled :", is_enrolled, "      | Type:", type(is_enrolled))

# Dynamic re-assignment: Variable type can change at runtime
data = 100
print("\nInitial data value:", data, "| Type:", type(data))
data = "Now I am a string"
print("Reassigned data   :", data, "| Type:", type(data))


print("\n" + "=" * 60)
print("PART 2: Multiple Assignments & Variable Swapping")
print("=" * 60)

# Assigning multiple variables in a single line
x, y, z = 10, 20, 30
print(f"Multiple assignment: x = {x}, y = {y}, z = {z}")

# Swapping values without a temporary variable
a, b = 5, 95
print(f"Before swap: a = {a}, b = {b}")
a, b = b, a
print(f"After swap : a = {a}, b = {b}")


print("\n" + "=" * 60)
print("PART 3: Type Casting & String Formatting")
print("=" * 60)

# Type casting (converting types explicitly)
str_num = "450"
num = int(str_num)          # Convert string to integer
float_num = float(num)      # Convert integer to float

print("Original String  :", repr(str_num), "| Type:", type(str_num))
print("Converted Integer:", num, "         | Type:", type(num))
print("Converted Float  :", float_num, "     | Type:", type(float_num))

# String Formatting using F-Strings (Python 3.6+)
course = "AI & Machine Learning"
duration_months = 6
cost = 499.99

formatted_summary = f"Course: {course}\nDuration: {duration_months} months\nTotal Fee: ${cost:.2f}"
print("\nFormatted Summary:\n" + formatted_summary)


print("\n" + "=" * 60)
print("PRACTICE PROBLEMS & SAMPLE SOLUTIONS")
print("=" * 60)

# Problem 1: Temperature Converter (Celsius to Fahrenheit)
# Formula: F = (C * 9/5) + 32
celsius = 25.0
fahrenheit = (celsius * 9 / 5) + 32
print(f"Problem 1: {celsius} deg C is equal to {fahrenheit} deg F")

# Problem 2: User Profile Card Generator
user_name = "Janani"
role = "AI/ML Learner"
projects_completed = 3
score = 94.5

print(f"\nProblem 2: User Profile Card")
print(f"  Name     : {user_name}")
print(f"  Role     : {role}")
print(f"  Projects : {projects_completed}")
print(f"  Score    : {score}%")
