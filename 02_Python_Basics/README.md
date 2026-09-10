# Python Basics Guide

Welcome to the **Python Basics** module of the AI & ML Learning journey! Python is the primary language used in Artificial Intelligence, Machine Learning, Data Science, and Deep Learning due to its readability, simplicity, and powerful ecosystem of libraries.

This folder contains theoretical notes, syntax summaries, and executable Python sample programs covering foundational programming concepts.

---

## Folder Structure

```text
02_Python_Basics/
├── README.md           # Detailed explanation of Python basics concepts
├── variables.py        # Variables, dynamic typing, scoping & formatting
├── data_types.py       # Built-in data types, type casting & string operations
├── conditions.py      # Conditional statements (if, elif, else) & logic
├── loops.py            # Iteration using for & while loops, control flow
├── lists.py            # Sequence data handling, slicing & list comprehensions
├── dictionaries.py     # Key-value maps, tuples & set data structures
└── functions.py        # Modular code using def, arguments, scope & lambda
```

---

## Core Topics Covered

### 1. Variables & Naming Conventions (`variables.py`)
- **Variables** act as containers for storing data values. In Python, variables are created automatically when you assign a value using the `=` operator.
- **Dynamic Typing:** Python does not require explicit declaration of variable types; the type is inferred at runtime.
- **Naming Rules & Conventions:**
  - Must begin with a letter or underscore (`_`).
  - Cannot begin with a number or use reserved keywords (e.g., `for`, `if`, `class`).
  - Use `snake_case` for multi-word variable names (e.g., `user_age`, `total_score`).
- **Key Concepts:** Reassignment, multiple assignment (`a, b = 1, 2`), variable swapping (`a, b = b, a`), constants (by convention using `UPPERCASE`), and f-string formatting.

### 2. Data Types & Operations (`data_types.py`)
Python provides several built-in data types grouped into categories:

| Category | Data Type | Example | Description |
| :--- | :--- | :--- | :--- |
| **Numeric** | `int`, `float`, `complex` | `42`, `3.14`, `2 + 3j` | Whole numbers, decimals, complex numbers |
| **Text** | `str` | `"Hello AI"` | Sequence of characters |
| **Boolean** | `bool` | `True`, `False` | Truth values for logical operations |
| **Sequence** | `list`, `tuple`, `range` | `[1, 2]`, `(1, 2)` | Ordered collections of items |
| **Mapping** | `dict` | `{"key": "value"}` | Key-value pairs |
| **Set** | `set` | `{1, 2, 3}` | Unordered collections of unique items |

- **Type Conversion (Casting):** Implicit conversion done by Python vs. explicit conversion using built-in functions (`int()`, `float()`, `str()`, `bool()`).
- **String Manipulations:** Immutability, indexing, slicing `[start:stop:step]`, and common methods (`.upper()`, `.lower()`, `.strip()`, `.replace()`, `.split()`, `.join()`).

### 3. Conditional Statements (`conditions.py`)
- Decision making in Python is controlled using `if`, `elif` (else if), and `else` statements based on boolean expressions.
- **Comparison Operators:** `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Logical Operators:** `and` (both true), `or` (at least one true), `not` (reverses truth value).
- **Ternary Operator:** Shortened conditional expression syntax: `value_if_true if condition else value_if_false`.

### 4. Control Flow & Loops (`loops.py`)
- **`for` Loops:** Used for iterating over a sequence (list, tuple, dictionary, set, or string) or numeric range using `range(start, stop, step)`.
- **`while` Loops:** Executes a block of code repeatedly as long as a given condition remains `True`.
- **Loop Control Statements:**
  - `break`: Terminate the loop immediately.
  - `continue`: Skip the rest of the current iteration and move to the next.
  - `pass`: Placeholder statement that does nothing.
- **Loop `else` Clause:** Executes when the loop finishes normally without encountering a `break`.

### 5. Lists & Sequenced Data (`lists.py`)
- **Lists** are ordered, mutable (modifiable), and heterogenous collections of elements defined using square brackets `[]`.
- **Operations:**
  - Accessing items via zero-based indexing (`list[0]`) and negative indexing (`list[-1]`).
  - Slicing (`list[start:stop:step]`).
  - Common Methods: `.append()`, `.extend()`, `.insert()`, `.pop()`, `.remove()`, `.sort()`, `.reverse()`.
- **List Comprehension:** Concise syntax for creating new lists: `[expression for item in iterable if condition]`.

### 6. Dictionaries, Tuples & Sets (`dictionaries.py`)
- **Dictionaries (`dict`):** Unordered/ordered (Python 3.7+) mutable collection of key-value pairs (`{key: value}`). Fast lookup by key.
- **Tuples (`tuple`):** Immutable ordered sequences defined using parentheses `()`. Used for fixed data that should not change. Supports unpacking (`x, y = point`).
- **Sets (`set`):** Unordered collection of unique items defined using `{}` or `set()`. Useful for removing duplicates and mathematical set operations (union, intersection, difference).

### 7. Functions & Scope (`functions.py`)
- **Functions** are reusable blocks of code that perform a specific task, defined using the `def` keyword.
- **Parameters & Arguments:** Positional arguments, keyword arguments, default parameter values (`def func(x=10)`).
- **Arbitrary Arguments:** `*args` (non-keyword variable length) and `**kwargs` (keyword variable length).
- **Scope:** Local variables (accessible inside function) vs Global variables (accessible module-wide).
- **Lambda Functions:** Anonymous single-line functions created using `lambda arguments: expression`.

---

## Sample Programs Summary

| Program File | Core Demonstration | Practice Problems Included |
| :--- | :--- | :--- |
| [`variables.py`](file:///c:/Users/JANANI/OneDrive/Desktop/AI-ML%20Task%201/AI-ML-Learning/02_Python_Basics/variables.py) | Variable assignment, dynamic typing, casting & f-strings | Variable Swapping, Temperature Converter, User Profile Generator |
| [`data_types.py`](file:///c:/Users/JANANI/OneDrive/Desktop/AI-ML%20Task%201/AI-ML-Learning/02_Python_Basics/data_types.py) | Primitive data types, type conversions & string methods | Type Identification, Sentence Formatter, Word Reverser |
| [`conditions.py`](file:///c:/Users/JANANI/OneDrive/Desktop/AI-ML%20Task%201/AI-ML-Learning/02_Python_Basics/conditions.py) | Decision branching, logical operators & ternary expressions | Even/Odd Check, Positive/Negative/Zero, Student Grading System, Leap Year Checker |
| [`loops.py`](file:///c:/Users/JANANI/OneDrive/Desktop/AI-ML%20Task%201/AI-ML-Learning/02_Python_Basics/loops.py) | `for` & `while` loops, control statements (`break`/`continue`) | Multiplication Table, Sum of N Numbers, Prime Number Checker, Pattern Printing |
| [`lists.py`](file:///c:/Users/JANANI/OneDrive/Desktop/AI-ML%20Task%201/AI-ML-Learning/02_Python_Basics/lists.py) | List manipulation, slicing, methods & list comprehension | Max/Min Finder, Filter Even Numbers, List Reversal, 2D Matrix Sum |
| [`dictionaries.py`](file:///c:/Users/JANANI/OneDrive/Desktop/AI-ML%20Task%201/AI-ML-Learning/02_Python_Basics/dictionaries.py) | Key-value pairs, immutable tuples & unique set operations | Word Frequency Counter, Student Record Lookup, Set Duplicate Remover |
| [`functions.py`](file:///c:/Users/JANANI/OneDrive/Desktop/AI-ML%20Task%201/AI-ML-Learning/02_Python_Basics/functions.py) | Function definitions, arguments, return values & recursion | Basic Calculator, Factorial Calculator, Palindrome Checker, Lambda Sorter |

---

## How to Run the Programs

You can run any script individually using your terminal or command prompt:

```bash
# Navigate to the Python Basics directory
cd "02_Python_Basics"

# Run a specific script
python variables.py
python data_types.py
python conditions.py
python loops.py
python lists.py
python dictionaries.py
python functions.py
```
