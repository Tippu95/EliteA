import pandas as pd
import pytest

# Load the test cases
age_category_test_cases = pd.read_csv('demo/Testcases/age_category_test_cases_updated.csv')

# Load the source data
source_data = pd.read_excel('demo/data/Clinical_Data_Validation_Cohort.xlsx')

# Load the target data
age_category_data = pd.read_csv('demo/Verify/age_category_data.csv')

# Function to determine age category
def determine_age_category(age):
    if age < 12:
        return 'Childhood'
    elif 12 <= age <= 20:
        return 'Teenage'
    elif 21 <= age <= 60:
        return 'Adult'
    else:
        return 'Old'

@pytest.mark.parametrize("index, row", age_category_test_cases.iterrows())
def test_category_match(index, row):
    patient_id = row['Patient ID']
    expected_category = row['Expected Age Category']
    actual_category = age_category_data.loc[age_category_data['Patient ID'] == patient_id, 'Age Category'].values[0]
    assert actual_category == expected_category, f"Mismatch for Patient ID {patient_id}: expected {expected_category}, got {actual_category}"

@pytest.mark.parametrize("index, row", source_data.iterrows())
def test_age_category_childhood(index, row):
    if row['Age'] < 12:
        assert determine_age_category(row['Age']) == 'Childhood'

@pytest.mark.parametrize("index, row", source_data.iterrows())
def test_age_category_teenage(index, row):
    if 12 <= row['Age'] <= 20:
        assert determine_age_category(row['Age']) == 'Teenage'

@pytest.mark.parametrize("index, row", source_data.iterrows())
def test_age_category_adult(index, row):
    if 21 <= row['Age'] <= 60:
        assert determine_age_category(row['Age']) == 'Adult'

@pytest.mark.parametrize("index, row", source_data.iterrows())
def test_age_category_old(index, row):
    if row['Age'] > 60:
        assert determine_age_category(row['Age']) == 'Old'

@pytest.mark.parametrize("index, row", age_category_test_cases.iterrows())
def test_patient_id_mapping(index, row):
    patient_id = row['Patient ID']
    assert patient_id in age_category_data['Patient ID'].values, f"Patient ID {patient_id} not found in target data"