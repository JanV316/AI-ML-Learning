# loops.py
# Python Basics: Loops, Iteration, and Control Statements
# --------------------------------------------------------
# Explanation:
# Loops allow a block of code to execute repeatedly.
# 1. 'for' loop: Iterates over a sequence (list, string, range, etc.) for a fixed number of times.
# 2. 'while' loop: Executes as long as a specified boolean condition is True.
# 3. Control statements:
#    - 'break'    : Terminates the loop completely.
#    - 'continue' : Skips the remaining statement in the current iteration.
#    - 'pass'     : Null statement (placeholder).

print("=" * 60)
print("PART 1: 'for' Loops & range() Function")
print("=" * 60)

# Syntax: range(start, stop, step)
print("Iterating over range(1, 6):")
for i in range(1, 6):
    print(f"  Iteration {i}")

print("\nIterating over range(10, 0, -2) (Countdown):")
for count in range(10, 0, -2):
    print(f"  Count: {count}")

# Iterating over string characters
tech_stack = "Python"
print(f"\nIterating over string '{tech_stack}':")
for char in tech_stack:
    print(f"  Character: {char}")


print("\n" + "=" * 60)
print("PART 2: 'while' Loops & Loop Control (break, continue)")
print("=" * 60)

# 'while' loop demonstration
counter = 1
print("Basic while loop counter:")
while counter <= 3:
    print(f"  Counter value: {counter}")
    counter += 1

# 'continue' and 'break' statements
print("\nDemonstrating 'continue' (skipping 3) and 'break' (stopping at 6):")
num = 0
while num < 10:
    num += 1
    if num == 3:
        print("  -> Skipping 3 (continue)")
        continue
    if num == 6:
        print("  -> Stopping loop at 6 (break)")
        break
    print(f"  Processed number: {num}")

# Loop 'else' clause: Executes if loop completes without a 'break'
print("\nLoop 'else' clause example:")
for item in [1, 2, 3]:
    print(f"  Processing item: {item}")
else:
    print("  -> Loop completed successfully without break!")


print("\n" + "=" * 60)
print("PART 3: Solved Practice Problems")
print("=" * 60)

# Problem 1: Multiplication Table
def print_multiplication_table(number, upto=5):
    print(f"Multiplication Table for {number}:")
    for i in range(1, upto + 1):
        print(f"  {number} x {i:<2} = {number * i}")

print("Problem 1: Multiplication Table")
print_multiplication_table(7, upto=5)

# Problem 2: Sum of First N Natural Numbers
def sum_n_numbers(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

print("\nProblem 2: Accumulator Pattern")
print("  Sum of numbers 1 to 100:", sum_n_numbers(100))

# Problem 3: Prime Number Checker
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

print("\nProblem 3: Prime Number Verification")
sample_nums = [2, 11, 15, 29, 33]
for n in sample_nums:
    result = "PRIME" if is_prime(n) else "NOT PRIME"
    print(f"  Number {n:<2} is {result}")

# Problem 4: Star Pattern Printing (Nested Loop)
print("\nProblem 4: Right-angled Triangle Pattern")
rows = 4
for i in range(1, rows + 1):
    print("  " + "* " * i)