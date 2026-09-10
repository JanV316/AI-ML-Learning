# dictionaries.py
# Python Basics: Dictionaries, Tuples, and Sets
# ----------------------------------------------
# Explanation:
# 1. Dictionary (dict): Key-value pair mapping, mutable, fast lookups using keys.
# 2. Tuple (tuple)    : Immutable ordered sequence, used for fixed structured data.
# 3. Set (set)        : Unordered collection of unique items, supports mathematical set operations.

print("=" * 60)
print("PART 1: Dictionaries (Key-Value Operations & Methods)")
print("=" * 60)

# Creating a dictionary
student_profile = {
    "id": "STU-101",
    "name": "Alex Johnson",
    "course": "AI & ML",
    "gpa": 3.9,
    "skills": ["Python", "Math", "SQL"]
}

print("Student Profile Dictionary:")
print(student_profile)

# Accessing Values
print("\nAccessing values:")
print("Name (using [] bracket)   :", student_profile["name"])
print("GPA (using .get() method) :", student_profile.get("gpa"))
print("Non-existent key (.get)   :", student_profile.get("age", "Key not found"))

# Modifying and Adding Entries
student_profile["gpa"] = 3.95                          # Update existing key
student_profile["email"] = "alex.j@example.com"        # Add new key
print("\nAfter updating GPA & adding Email:")
print("Updated Profile:", student_profile)

# Iterating through Dictionaries
print("\nIterating over Keys, Values, and Items:")
for key, value in student_profile.items():
    print(f"  {key:<8} -> {value}")


print("\n" + "=" * 60)
print("PART 2: Tuples (Immutable Sequences & Unpacking)")
print("=" * 60)

# Creating tuples
coordinates = (37.7749, -122.4194)  # Latitude, Longitude (SF)
color_rgb = (255, 128, 0)

print("Coordinates Tuple:", coordinates)
print("RGB Color Tuple  :", color_rgb)

# Tuple Unpacking
lat, lon = coordinates
print(f"\nUnpacked Values -> Latitude: {lat}, Longitude: {lon}")

# Tuple Immutability Check (uncommenting below raises TypeError)
# coordinates[0] = 40.7128  # TypeError: 'tuple' object does not support item assignment
print("Tuples cannot be modified after creation (Immutable).")


print("\n" + "=" * 60)
print("PART 3: Sets (Unique Collections & Set Operations)")
print("=" * 60)

# Creating sets (automatically removes duplicates)
dataset_a = {1, 2, 3, 4, 5, 5, 5}
dataset_b = {4, 5, 6, 7, 8}

print("Dataset A (Deduplicated):", dataset_a)
print("Dataset B               :", dataset_b)

# Set Mathematical Operations
print("\nSet Operations:")
print("Union (A | B)        :", dataset_a.union(dataset_b))
print("Intersection (A & B) :", dataset_a.intersection(dataset_b))
print("Difference (A - B)   :", dataset_a.difference(dataset_b))


print("\n" + "=" * 60)
print("PART 4: Solved Practice Problems")
print("=" * 60)

# Problem 1: Word Frequency Counter (Dictionary application)
text = "python is easy python is powerful machine learning uses python"

def count_word_frequency(sentence):
    words = sentence.split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

freq_dict = count_word_frequency(text)
print("Problem 1: Word Frequency Counter")
print("  Text Sample:", repr(text))
print("  Word Counts:")
for w, count in freq_dict.items():
    print(f"    '{w}': {count}")

# Problem 2: Remove Duplicates from List using Set
raw_tags = ["AI", "ML", "Python", "AI", "Data", "ML", "Python"]
unique_tags = list(set(raw_tags))

print("\nProblem 2: Set Deduplication")
print("  Raw Tags   :", raw_tags)
print("  Unique Tags:", unique_tags)

# Problem 3: Student Marks Lookup & Grade Calculation
class_records = {
    "Sonia": [85, 90, 92],
    "Rohan": [70, 75, 78],
    "Kiran": [95, 98, 92]
}

print("\nProblem 3: Student Class Records (Average Score)")
for name, marks in class_records.items():
    avg = sum(marks) / len(marks)
    print(f"  Student: {name:<6} | Average Marks: {avg:.2f}")
