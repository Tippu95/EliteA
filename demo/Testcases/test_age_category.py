import pytest
import pandas as pd

# Load the data
data = pd.read_csv('../Verify/age_category_data.csv')

# Test cases
test_cases = [
    (10, 'Childhood'),
    (15, 'Teenage'),
    (30, 'Adult'),
    (65, 'Old'),
    (None, None)
]

@pytest.mark.parametrize("age, expected_category", test_cases)
def test_age_category(age, expected_category):
    if age is not None:
        result = data[data['age'] == age]['age_category'].values[0]
    else:
        result = data[data['age'].isnull()]['age_category'].values[0]
    assert result == expected_category, f"Expected {expected_category}, but got {result}"

if __name__ == "__main__":
    pytest.main()
