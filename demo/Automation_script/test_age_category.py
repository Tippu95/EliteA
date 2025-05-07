import pytest
import pandas as pd

# Load test cases and verification data
age_category_test_cases = pd.read_csv('demo/Testcases/age_category_test_cases.csv')
age_category_data = pd.read_csv('demo/Verify/age_category_data.csv')

@pytest.mark.parametrize("test_case_id, age, expected_category", [
    ("TC_01", 10, "Childhood"),
    ("TC_02", 15, "Teenage"),
    ("TC_03", 30, "Adult"),
    ("TC_04", 65, "Old"),
    ("TC_05", None, None)
])
def test_age_category(test_case_id, age, expected_category):
    if age is not None:
        result = age_category_data[age_category_data['Age'] == age]['Age Category'].values[0]
    else:
        result = age_category_data[age_category_data['Age'].isnull()]['Age Category'].values[0]
    assert result == expected_category, f"Test Case {test_case_id} failed: expected {expected_category}, got {result}"

if __name__ == '__main__':
    pytest.main()
