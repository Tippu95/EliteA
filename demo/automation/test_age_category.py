import pytest
import pandas as pd

# Constants
SOURCE_PATH = "demo/data/Clinical_Data_Validation_Cohort.xlsx"
TARGET_PATH = "demo/Verify/age_category_data.csv"

# Functions

def load_data(source_path, target_path):
    source_df = pd.read_excel(source_path)
    target_df = pd.read_csv(target_path)
    return source_df, target_df

def merge_data(source_df, target_df, join_column="Patient ID"):
    return pd.merge(source_df, target_df, on=join_column, how="inner")

def compute_age_category(age):
    if age <= 11:
        return "Childhood"
    elif 12 <= age <= 20:
        return "Teenage"
    elif 21 <= age <= 60:
        return "Adult"
    else:
        return "Old"

def process_data(merged_df):
    merged_df["Computed Age Category"] = merged_df["Age"].apply(compute_age_category)
    merged_df["Category Match"] = merged_df["Computed Age Category"] == merged_df["Age Category"]
    return merged_df

def validate_data(merged_df):
    return merged_df["Category Match"].all()

@pytest.fixture
def setup_data():
    source_df, target_df = load_data(SOURCE_PATH, TARGET_PATH)
    merged_df = merge_data(source_df, target_df)
    processed_df = process_data(merged_df)
    return processed_df

def test_category_match(setup_data):
    processed_df = setup_data
    assert validate_data(processed_df), "Computed age categories do not match Age Categories in some rows."

def test_age_category_childhood(setup_data):
    processed_df = setup_data
    childhood_df = processed_df[processed_df['Age'] <= 11]
    assert (childhood_df['Age Category'] == 'Childhood').all(), "Some 'Childhood' age categories are incorrect."

def test_age_category_teenage(setup_data):
    processed_df = setup_data
    teenage_df = processed_df[(processed_df['Age'] >= 12) & (processed_df['Age'] <= 20)]
    assert (teenage_df['Age Category'] == 'Teenage').all(), "Some 'Teenage' age categories are incorrect."

def test_age_category_adult(setup_data):
    processed_df = setup_data
    adult_df = processed_df[(processed_df['Age'] >= 21) & (processed_df['Age'] <= 60)]
    assert (adult_df['Age Category'] == 'Adult').all(), "Some 'Adult' age categories are incorrect."

def test_age_category_old(setup_data):
    processed_df = setup_data
    old_df = processed_df[processed_df['Age'] > 60]
    assert (old_df['Age Category'] == 'Old').all(), "Some 'Old' age categories are incorrect."

def test_patient_id_mapping(setup_data):
    processed_df = setup_data
    source_df, target_df = load_data(SOURCE_PATH, TARGET_PATH)
    assert set(source_df['Patient ID']) == set(target_df['Patient ID']), "Patient ID mapping between files is incorrect."
