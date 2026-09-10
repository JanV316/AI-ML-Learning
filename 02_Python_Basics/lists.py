# lists.py
# Python Basics: Lists, Slicing, Methods, and List Comprehensions
# ----------------------------------------------------------------
# Explanation:
# A list in Python is an ordered, mutable (changeable) collection of items.
# Lists are created using square brackets `[]`.
# Lists can contain items of different data types (heterogeneous) and duplicate elements.

print("=" * 60)
print("PART 1: List Creation, Indexing, and Slicing")
print("=" * 60)

# Creating lists
numbers = [10, 20, 30, 40, 50, 60]
mixed_list = ["Python", 3.14, 2026, True, [1, 2]]

print("Numbers List:", numbers)
print("Mixed List  :", mixed_list)

# Indexing (Zero-based and Negative indexing)
print("\nIndexing Examples:")
print("First Element (numbers[0])   :", numbers[0])
print("Last Element (numbers[-1])   :", numbers[-1])
print("Third Element (numbers[2])   :", numbers[2])

# Slicing: list[start:stop:step]
print("\nSlicing Examples:")
print("Sub-list [1:4]               :", numbers[1:4])
print("First 3 elements [:3]        :", numbers[:3])
print("From index 3 onwards [3:]    :", numbers[3:])
print("Every second element [::2]   :", numbers[::2])
print("Reversed List [::-1]         :", numbers[::-1])


print("\n" + "=" * 60)
print("PART 2: Built-in List Methods & Operations")
print("=" * 60)

fruits = ["apple", "banana", "cherry"]
print("Initial Fruits List:", fruits)

# Adding elements
fruits.append("orange")         # Add to end
print("After append('orange')     :", fruits)

fruits.insert(1, "mango")       # Insert at index 1
print("After insert(1, 'mango')   :", fruits)

fruits.extend(["grape", "kiwi"])# Extend with another list
print("After extend(['grape','kiwi']):", fruits)

# Removing elements
popped_item = fruits.pop()      # Removes and returns last item
print(f"Popped item: '{popped_item}' | List after pop():", fruits)

fruits.remove("banana")         # Removes first occurrence of 'banana'
print("After remove('banana')     :", fruits)

# Sorting and Reversing
fruits.sort()                   # Alphabetical sort (in-place)
print("After sort()               :", fruits)

fruits.reverse()                # Reverse in-place
print("After reverse()            :", fruits)


print("\n" + "=" * 60)
print("PART 3: List Comprehensions & 2D Matrices")
print("=" * 60)

# List Comprehension Syntax: [expression for item in iterable if condition]
numbers_1_10 = list(range(1, 11))
print("Original Numbers:", numbers_1_10)

# Squares of even numbers only
even_squares = [x**2 for x in numbers_1_10 if x % 2 == 0]
print("Squares of Even Numbers (Comprehension):", even_squares)

# 2D Matrix (List of Lists)
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("\n2D Matrix Traversal:")
for row in matrix:
    print(" ", row)

print("Accessing Element at Matrix Row 1, Col 2 (matrix[1][2]):", matrix[1][2])


print("\n" + "=" * 60)
print("PART 4: Solved Practice Problems")
print("=" * 60)

# Problem 1: Find Maximum, Minimum, and Average of a List
sample_scores = [78, 92, 85, 64, 99, 88, 71]

def analyze_scores(scores):
    max_val = max(scores)
    min_val = min(scores)
    avg_val = sum(scores) / len(scores)
    return max_val, min_val, avg_val

max_s, min_s, avg_s = analyze_scores(sample_scores)
print("Problem 1: List Statistics")
print("  Scores List:", sample_scores)
print(f"  Max Score  : {max_s}")
print(f"  Min Score  : {min_s}")
print(f"  Average    : {avg_s:.2f}")

# Problem 2: Remove Duplicates from List (Preserving Order)
raw_list = [10, 20, 10, 30, 40, 20, 50, 10]

def remove_duplicates(lst):
    unique_lst = []
    for item in lst:
        if item not in unique_lst:
            unique_lst.append(item)
    return unique_lst

print("\nProblem 2: Remove Duplicates")
print("  Raw List   :", raw_list)
print("  Unique List:", remove_duplicates(raw_list))

# Problem 3: Flatten a Nested List
nested_list = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flattened = [item for sublist in nested_list for item in sublist]

print("\nProblem 3: Flatten Nested List")
print("  Nested List   :", nested_list)
print("  Flattened List:", flattened)
