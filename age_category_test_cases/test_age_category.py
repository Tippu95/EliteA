import pytest

# Sample data representing the table in Microsoft Fabric
data = [
    {"name": "Alice", "age": 5},
    {"name": "Bob", "age": 16},
    {"name": "Charlie", "age": 25},
    {"name": "David", "age": 70},
]

# Function to categorize age
def categorize_age(age):
    if age <= 12:
        return "Child"
    elif age <= 19:
        return "Teen"
    elif age <= 64:
        return "Adult"
    else:
        return "Senior"

# Test cases
@pytest.mark.parametrize("age, expected_category", [
    (5, "Child"),
    (16, "Teen"),
    (25, "Adult"),
    (70, "Senior"),
])
def test_age_category(age, expected_category):
    assert categorize_age(age) == expected_category

# Instructions for executing the code:
# 1. Save this script as test_age_category.py
# 2. Open a terminal and navigate to the directory containing the script.
# 3. Run the tests using the command: pytest test_age_category.py

# Note: Ensure that pytest is installed in your environment. You can install it using `pip install pytest`.