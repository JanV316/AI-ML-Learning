# functions.py
# Python Basics: Functions, Arguments, Scope, and Lambda Expressions
# ------------------------------------------------------------------
# Explanation:
# A function is a block of organized, reusable code used to perform a single related action.
# Syntax:
#   def function_name(parameters):
#       """Docstring explaining the function."""
#       # statements
#       return expression

print("=" * 60)
print("PART 1: Function Definition, Parameters & Return Values")
print("=" * 60)

def greet_user(name, title="Learner"):
    """Greets a user with a title and returns the greeting string."""
    return f"Welcome, {title} {name}! Ready to explore Python for AI/ML."

# Positional and Keyword arguments
greeting1 = greet_user("Janani")                       # Uses default title
greeting2 = greet_user(name="Dr. Smith", title="Prof.") # Keyword arguments

print("Greeting 1:", greeting1)
print("Greeting 2:", greeting2)


print("\n" + "=" * 60)
print("PART 2: Arbitrary Arguments (*args & **kwargs)")
print("=" * 60)

# *args: Accepts any number of positional arguments as a tuple
def calculate_sum(*numbers):
    """Calculates the sum of arbitrary numbers passed as arguments."""
    total = sum(numbers)
    return total

print("Sum of (10, 20, 30)       :", calculate_sum(10, 20, 30))
print("Sum of (5, 15, 25, 35, 45) :", calculate_sum(5, 15, 25, 35, 45))

# **kwargs: Accepts any number of keyword arguments as a dictionary
def print_user_details(**kwargs):
    """Prints arbitrary key-value metadata of a user."""
    print("User Details:")
    for key, val in kwargs.items():
        print(f"  {key:<10}: {val}")

print_user_details(name="Maya", role="Data Scientist", experience="3 years", location="Bangalore")


print("\n" + "=" * 60)
print("PART 3: Scope & Anonymous Lambda Functions")
print("=" * 60)

# Local vs Global Scope
global_counter = 100  # Global variable

def modify_scope_demo():
    local_val = 50     # Local variable
    print(f"Inside function -> Local: {local_val}, Global: {global_counter}")

modify_scope_demo()

# Lambda Functions: Syntax -> lambda arguments : expression
square = lambda x: x ** 2
multiply = lambda a, b: a * b

print("\nLambda Functions Examples:")
print("Square of 8        :", square(8))
print("Multiply 6 x 7     :", multiply(6, 7))

# Lambda used inside built-in functions like map, filter, sorted
nums = [1, 5, 2, 8, 3]
sorted_nums = sorted(nums, key=lambda x: x)
even_only = list(filter(lambda x: x % 2 == 0, nums))

print("Filtered Evens     :", even_only)


print("\n" + "=" * 60)
print("PART 4: Solved Practice Problems")
print("=" * 60)

# Problem 1: Basic Calculator Function
def calculator(a, b, operation="+"):
    """Performs basic arithmetic operations (+, -, *, /)."""
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        return a / b if b != 0 else "Error: Division by zero"
    else:
        return "Error: Invalid operation"

print("Problem 1: Basic Calculator")
print("  15 + 5 =", calculator(15, 5, "+"))
print("  15 * 4 =", calculator(15, 4, "*"))
print("  20 / 0 =", calculator(20, 0, "/"))

# Problem 2: Factorial (Iterative & Recursive)
def factorial_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def factorial_recursive(n):
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)

print("\nProblem 2: Factorial Calculation")
print("  Factorial of 5 (Iterative) :", factorial_iterative(5))
print("  Factorial of 5 (Recursive) :", factorial_recursive(5))

# Problem 3: Palindrome Checker Function
def is_palindrome_sentence(sentence):
    cleaned = "".join(char.lower() for char in sentence if char.isalnum())
    return cleaned == cleaned[::-1]

print("\nProblem 3: Sentence Palindrome Checker")
sample1 = "A man, a plan, a canal: Panama"
sample2 = "Hello World"
print(f"  '{sample1}' -> {is_palindrome_sentence(sample1)}")
print(f"  '{sample2}' -> {is_palindrome_sentence(sample2)}")

# Problem 4: Maximum of Three Numbers
def find_max_of_three(a, b, c):
    return max(a, b, c)

print("\nProblem 4: Maximum of Three Numbers")
print("  Max of (45, 89, 23) ->", find_max_of_three(45, 89, 23))
