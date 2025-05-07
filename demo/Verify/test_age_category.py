import pytest
import sqlite3

# Database connection setup
@pytest.fixture(scope='module')
def db_connection():
    conn = sqlite3.connect(':memory:')  # Using in-memory database for testing
    cursor = conn.cursor()
    # Create table and insert test data
    cursor.execute('''
    CREATE TABLE Clinical_Data_Validation_Cohort (
        age INTEGER,
        age_category TEXT
    )
    ''')
    cursor.executemany('''
    INSERT INTO Clinical_Data_Validation_Cohort (age, age_category) VALUES (?, ?)
    ''', [
        (10, 'Childhood'),
        (15, 'Teenage'),
        (30, 'Adult'),
        (65, 'Old'),
        (None, None)
    ])
    conn.commit()
    yield conn
    conn.close()

# Test cases
@pytest.mark.parametrize('age, expected_category', [
    (10, 'Childhood'),
    (15, 'Teenage'),
    (30, 'Adult'),
    (65, 'Old'),
    (None, None)
])
def test_age_category(db_connection, age, expected_category):
    cursor = db_connection.cursor()
    if age is not None:
        cursor.execute('SELECT age_category FROM Clinical_Data_Validation_Cohort WHERE age = ?', (age,))
    else:
        cursor.execute('SELECT age_category FROM Clinical_Data_Validation_Cohort WHERE age IS NULL')
    result = cursor.fetchone()
    assert result[0] == expected_category
