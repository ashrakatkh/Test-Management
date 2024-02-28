import sqlite3

def create_database():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('test_management.db')
    cursor = conn.cursor()

    # Create the TestAssets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TestAssets (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT
        )
    ''')

    # Create the TestCases table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TestCases (
            id INTEGER PRIMARY KEY,
            testAssetId INTEGER,
            name TEXT,
            description TEXT,
            FOREIGN KEY (testAssetId) REFERENCES TestAssets(id)
        )
    ''')

    # Create the ExecutionResults table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ExecutionResults (
            id INTEGER PRIMARY KEY,
            testCaseId INTEGER,
            result TEXT,
            executionDate TEXT,
            FOREIGN KEY (testCaseId) REFERENCES TestCases(id)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def insert_data():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('test_management.db')
    cursor = conn.cursor()

    # Insert a test asset
    cursor.execute('''
        INSERT INTO TestAssets (name, description)
        VALUES (?, ?)
    ''', ('TestAsset1', 'This is the first test asset'))

    test_asset_id = cursor.lastrowid

    # Insert a test case associated with the test asset
    cursor.execute('''
        INSERT INTO TestCases (testAssetId, name, description)
        VALUES (?, ?, ?)
    ''', (test_asset_id, 'TestCase1', 'This is the first test case for TestAsset1'))

    test_case_id = cursor.lastrowid

    # Insert the execution result for the test case
    cursor.execute('''
        INSERT INTO ExecutionResults (testCaseId, result, executionDate)
        VALUES (?, ?, ?)
    ''', (test_case_id, 'Passed', '2024-02-25'))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()



# Create the database
create_database()

# Insert data into the database
insert_data()

