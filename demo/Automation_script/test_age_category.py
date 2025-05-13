import pytest
import pandas as pd

# ========= Constants ============
SOURCE_PATH = "../data/Clinical_Data_Validation_Cohort.xlsx"
TARGET_PATH = "../Verify/age_category_data.csv"


# ========= Functions ============

def load_data(source_path, target_path):
    """
    Loads source and target data from the provided paths.
    """
    df1 = pd.read_excel(source_path)
    df2 = pd.read_csv(target_path)
    return df1, df2


def merge_data(source_df, target_df, join_column="Patient ID"):
    """
    Merges source and target data on the specified column.
    """
    return pd.merge(source_df, target_df, on=join_column, how="inner")


def compute_age_category(age):
    """
    Computes age category based on the age column.
    """
    if age < 12:
        return "Childhood"
    elif 12 <= age < 21:
        return "Teenage"
    elif 21 <= age < 61:
        return "Adult"
    else:
        return "Old"


def process_data(merged_df):
    """
    Processes data to compute age categories and check category matching.
    """
    # Compute the computed age category column
    merged_df["Computed Age Category"] = merged_df["Age"].apply(compute_age_category)

    # Add a flag column for category matching
    merged_df["Category Match"] = merged_df["Computed Age Category"] == merged_df["Age Category"]

    return merged_df


def validate_data(merged_df):
    """
    Validates that all rows have matching categories.
    Returns a boolean indicating success.
    """
    return merged_df["Category Match"].all()


# ========= Tests ============

@pytest.fixture
def setup_data():
    """
    Fixture to prepare and process data for testing.
    """
    source_df, target_df = load_data(SOURCE_PATH, TARGET_PATH)
    merged_df = merge_data(source_df, target_df)
    processed_df = process_data(merged_df)
    return processed_df


def test_category_match(setup_data):
    """
    Test to ensure every computed age category matches the target age category.
    """
    processed_df = setup_data
    assert validate_data(processed_df), "Computed age categories do not match Age Categories in some rows."


def test_age_category_childhood(setup_data):
    """
    Test to verify age category for age less than 12.
    """
    processed_df = setup_data
    childhood_df = processed_df[processed_df["Age"] < 12]
    assert (childhood_df["Computed Age Category"] == "Childhood").all(), "Childhood age category is incorrect."


def test_age_category_teenage(setup_data):
    """
    Test to verify age category for age between 12 and 20.
    """
    processed_df = setup_data
    teenage_df = processed_df[(processed_df["Age"] >= 12) & (processed_df["Age"] < 21)]
    assert (teenage_df["Computed Age Category"] == "Teenage").all(), "Teenage age category is incorrect."


def test_age_category_adult(setup_data):
    """
    Test to verify age category for age between 21 and 60.
    """
    processed_df = setup_data
    adult_df = processed_df[(processed_df["Age"] >= 21) & (processed_df["Age"] < 61)]
    assert (adult_df["Computed Age Category"] == "Adult").all(), "Adult age category is incorrect."


def test_age_category_old(setup_data):
    """
    Test to verify age category for age above 60.
    """
    processed_df = setup_data
    old_df = processed_df[processed_df["Age"] >= 61]
    assert (old_df["Computed Age Category"] == "Old").all(), "Old age category is incorrect."


