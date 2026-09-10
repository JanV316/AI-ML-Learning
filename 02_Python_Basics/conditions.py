# conditions.py
# Python Conditional Statements - Explanation and Practice Problems
# -----------------------------------------------------------------
# Explanation:
# Conditional statements allow programs to make decisions based on specified conditions.
# Syntax:
#   if condition:
#       # block of code
#   elif another_condition:
#       # block of code
#   else:
#       # default block of code
#
# Operators:
#   - Comparison: ==, !=, >, <, >=, <=
#   - Logical   : and, or, not

print("=" * 60)
print("PART 1: Basic & Nested Conditional Statements")
print("=" * 60)

# Demonstrating if-elif-else with a predefined test value
temperature = 28  # Celsius

print(f"Current Temperature: {temperature} deg C")
if temperature > 35:
    print("Weather Alert: Extreme heat! Stay hydrated.")
elif temperature >= 25:
    print("Weather Status: Warm and pleasant.")
elif temperature >= 15:
    print("Weather Status: Cool and breezy.")
else:
    print("Weather Status: Cold! Wear a jacket.")

# Nested Conditions
age = 20
has_license = True

print(f"\nNested Condition Check (Age: {age}, License: {has_license}):")
if age >= 18:
    if has_license:
        print("  -> Eligible to drive legally.")
    else:
        print("  -> Eligible by age, but needs a driving license.")
else:
    print("  -> Not eligible to drive.")


print("\n" + "=" * 60)
print("PART 2: Logical Operators & Ternary Expressions")
print("=" * 60)

# Logical Operators: AND, OR, NOT
score = 85
attendance = 92

print(f"Student Stats -> Score: {score}%, Attendance: {attendance}%")
if score >= 75 and attendance >= 80:
    print("  -> Honors Distinction: Qualified!")
else:
    print("  -> Honors Distinction: Not Qualified.")

# Ternary Conditional Operator (Short-hand syntax)
status = "Passed" if score >= 50 else "Failed"
print(f"Ternary evaluation result: {status}")


print("\n" + "=" * 60)
print("PART 3: Solved Practice Problems")
print("=" * 60)

# Problem 1: Even or Odd
def check_even_odd(num):
    if num % 2 == 0:
        return f"{num} is Even."
    else:
        return f"{num} is Odd."

print("Problem 1: Even or Odd Check")
print("  Sample (num = 7) :", check_even_odd(7))
print("  Sample (num = 14):", check_even_odd(14))

# Problem 2: Positive, Negative, or Zero
def check_sign(num):
    if num > 0:
        return f"{num} is Positive."
    elif num < 0:
        return f"{num} is Negative."
    else:
        return "The number is Zero."

print("\nProblem 2: Sign Identification")
print("  Sample (num = 15) :", check_sign(15))
print("  Sample (num = -8) :", check_sign(-8))
print("  Sample (num = 0)  :", check_sign(0))

# Problem 3: Student Grade Evaluation
def evaluate_grade(marks):
    if marks >= 90 and marks <= 100:
        return "Grade: A (Outstanding)"
    elif marks >= 80 and marks < 90:
        return "Grade: B (Very Good)"
    elif marks >= 70 and marks < 80:
        return "Grade: C (Good)"
    elif marks >= 50 and marks < 70:
        return "Grade: D (Satisfactory)"
    elif marks >= 0 and marks < 50:
        return "Grade: F (Fail)"
    else:
        return "Invalid Marks entered!"

print("\nProblem 3: Student Grade Calculator")
print("  Marks = 95 ->", evaluate_grade(95))
print("  Marks = 74 ->", evaluate_grade(74))
print("  Marks = 42 ->", evaluate_grade(42))

# Problem 4: Leap Year Checker
def is_leap_year(year):
    # A year is leap if divisible by 4, but not by 100 unless also divisible by 400
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return f"{year} IS a leap year."
    else:
        return f"{year} IS NOT a leap year."

print("\nProblem 4: Leap Year Verification")
print("  Year = 2024 ->", is_leap_year(2024))
print("  Year = 2023 ->", is_leap_year(2023))
print("  Year = 1900 ->", is_leap_year(1900))
print("  Year = 2000 ->", is_leap_year(2000))