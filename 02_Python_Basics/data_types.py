# data_types.py
# Python Basics: Data Types, Type Conversions, and String Operations
# ------------------------------------------------------------------
# Explanation:
# Data types define the type of data a variable can hold.
# Python has several built-in data types:
#   - Numeric: int, float, complex
#   - Text: str
#   - Boolean: bool (True / False)
#   - Sequence: list, tuple, range
#   - Mapping: dict
#   - Set: set, frozenset

print("=" * 60)
print("PART 1: Primitive Data Types & Type Inspection")
print("=" * 60)

num_int = 42
num_float = 3.14159
num_complex = 3 + 4j
text_str = "Artificial Intelligence"
is_active = True
empty_val = None

print(f"num_int     = {num_int:<22} | Type: {type(num_int)}")
print(f"num_float   = {num_float:<22} | Type: {type(num_float)}")
print(f"num_complex = {str(num_complex):<22} | Type: {type(num_complex)}")
print(f"text_str    = {text_str:<22} | Type: {type(text_str)}")
print(f"is_active   = {str(is_active):<22} | Type: {type(is_active)}")
print(f"empty_val   = {str(empty_val):<22} | Type: {type(empty_val)}")

# Checking types using isinstance()
print("\nType Verification with isinstance():")
print(f"Is num_int an integer? -> {isinstance(num_int, int)}")
print(f"Is text_str a string?  -> {isinstance(text_str, str)}")


print("\n" + "=" * 60)
print("PART 2: String Operations & Built-in String Methods")
print("=" * 60)

sample_text = "  python programming for Machine Learning  "

print("Original String    :", repr(sample_text))
print("Length of String   :", len(sample_text))
print("Stripped Whitespace:", repr(sample_text.strip()))
print("Uppercase          :", sample_text.upper().strip())
print("Lowercase          :", sample_text.lower().strip())
print("Title Case         :", sample_text.title().strip())
print("Replace Word       :", sample_text.replace("python", "Advanced Python").strip())

# Splitting and Joining Strings
words_list = sample_text.strip().split(" ")
print("Split into List    :", words_list)
rejoined = "-".join(words_list)
print("Joined with Hyphens:", rejoined)

# String Slicing [start:stop:step]
phrase = "DeepLearning"
print("\nString Slicing Examples:")
print("First 4 chars [0:4]  :", phrase[0:4])
print("From index 4 [4:]    :", phrase[4:])
print("Reverse string [::-1]:", phrase[::-1])


print("\n" + "=" * 60)
print("PART 3: Boolean Logic & Numeric Operations")
print("=" * 60)

# Truthiness in Python
print("Boolean Evaluation of values:")
print("bool(1)        ->", bool(1))
print("bool(0)        ->", bool(0))
print("bool('Hello')  ->", bool("Hello"))
print("bool('')       ->", bool(""))
print("bool([])       ->", bool([]))

# Common Numeric Operations
val_a = 17
val_b = 5

print(f"\nArithmetic Operations between {val_a} and {val_b}:")
print(f"Addition ({val_a} + {val_b})       = {val_a + val_b}")
print(f"Subtraction ({val_a} - {val_b})    = {val_a - val_b}")
print(f"Multiplication ({val_a} * {val_b}) = {val_a * val_b}")
print(f"Division ({val_a} / {val_b})       = {val_a / val_b}")
print(f"Floor Division ({val_a} // {val_b}) = {val_a // val_b}")
print(f"Modulus ({val_a} % {val_b})        = {val_a % val_b}")
print(f"Exponentiation ({val_a} ** {val_b}) = {val_a ** val_b}")


print("\n" + "=" * 60)
print("PRACTICE PROBLEMS & SAMPLE SOLUTIONS")
print("=" * 60)

# Problem 1: Word Count & Vowel Counter
sentence = "Machine learning algorithms learn from data."
vowels = "aeiouAEIOU"
vowel_count = sum(1 for char in sentence if char in vowels)
word_count = len(sentence.split())

print(f"Problem 1: Sentence Analysis")
print(f"  Sentence   : \"{sentence}\"")
print(f"  Word Count : {word_count}")
print(f"  Vowel Count: {vowel_count}")

# Problem 2: Palindrome String Checker
test_word = "radar"
is_palindrome = test_word.lower() == test_word.lower()[::-1]
print(f"\nProblem 2: Palindrome Checker")
print(f"  Word: '{test_word}' | Is Palindrome? -> {is_palindrome}")
