from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('test_management.db')
    except sqlite3.Error as e:
        print(e)
    return conn





# Create a new test case
@app.route('/testcases', methods=['POST'])
def create_test_case():
    conn = db_connection()
    cursor = conn.cursor()
    test_asset_name = request.json['test_asset_name']
    name = request.json['name']
    description = request.json['description']
    #result = request.json['result']
    #date = request.json['date']

    if not test_asset_name or not name or not description :
        return jsonify({'error': 'Test asset Name, name, description are required'}), 400

    # Check if the test asset already exists
    cursor.execute("SELECT id FROM TestAssets WHERE name = ?", (test_asset_name,))
    test_asset_id = cursor.fetchone()

    if not test_asset_id:
        # Insert a new test asset
        cursor.execute("INSERT INTO TestAssets (name) VALUES (?)", (test_asset_name,))
        test_asset_id = cursor.lastrowid
    else:
        test_asset_id = test_asset_id[0] 

    # Insert a test case associated with the test asset
    cursor.execute('''
        INSERT INTO TestCases (testAssetId, name, description)
        VALUES (?, ?, ?)
    ''', (test_asset_id, name, description))

    test_case_id = cursor.lastrowid

    # Insert the execution result for the test case
    #cursor.execute('''
        #INSERT INTO ExecutionResults (testCaseId, result, executionDate)
        #VALUES (?, ?, ?)
    #''', (test_case_id, result, date))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return jsonify({'message': 'Test case created successfully'}), 201
    
@app.route('/testcases', methods=['GET'])
def get_all_test_cases():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT tc.name, tc.description, er.result, er.executionDate
        FROM TestCases tc
        JOIN ExecutionResults er ON tc.id = er.testCaseId
    ''')

    test_cases = []
    rows = cursor.fetchall()
    for row in rows:
        test_case = {
            'name': row[0],
            'description': row[1],
            'result': row[2],
            'execution_date': row[3]
        }
        test_cases.append(test_case)

    conn.close()

    return jsonify(test_cases)


@app.route('/testcases/<int:testcase_id>', methods=['GET'])
def get_test_case(testcase_id):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT tc.name, tc.description, er.result, er.executionDate
        FROM TestCases tc
        JOIN ExecutionResults er ON tc.id = er.testCaseId
        WHERE tc.id = ?
    ''', (testcase_id,))

    row = cursor.fetchone()
    if row is None:
        return jsonify({'error': 'Test case not found'}), 404

    test_case = {
        'name': row[0],
        'description': row[1],
        'result': row[2],
        'execution_date': row[3]
    }

    conn.close()

    return jsonify(test_case)
    
@app.route('/testcases/<int:testcase_id>', methods=['PUT'])
def update_test_case(testcase_id):
    conn = db_connection()
    cursor = conn.cursor()

    # Retrieve the existing test case from the database
    cursor.execute('SELECT * FROM TestCases WHERE id = ?', (testcase_id,))
    test_case = cursor.fetchone()

    if test_case is None:
        return jsonify({'error': 'Test case not found'}), 404

    # Update the test case with the new data
    name = request.json.get('name', test_case[1])
    description = request.json.get('description', test_case[2])

    cursor.execute('''
        UPDATE TestCases
        SET name = ?, description = ?
        WHERE id = ?
    ''', (name, description, testcase_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return jsonify({'message': 'Test case updated successfully'}), 200

@app.route('/testcases/<int:testcase_id>', methods=['DELETE'])
def delete_test_case(testcase_id):
    conn = db_connection()
    cursor = conn.cursor()

    # Check if the test case exists
    cursor.execute('SELECT * FROM TestCases WHERE id = ?', (testcase_id,))
    test_case = cursor.fetchone()

    if test_case is None:
        return jsonify({'error': 'Test case not found'}), 404

    # Delete the test case from the TestCases table
    cursor.execute('DELETE FROM TestCases WHERE id = ?', (testcase_id,))

    # Delete the associated execution results from the ExecutionResults table
    cursor.execute('DELETE FROM ExecutionResults WHERE testCaseId = ?', (testcase_id,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return jsonify({'message': 'Test case deleted successfully'}), 200
    
@app.route('/testcases/addResults', methods=['POST'])
def record_execution_result():
    conn = db_connection()
    cursor = conn.cursor()

    # Retrieve the data from the request payload
    test_asset_name = request.json.get('test_asset_name')
    test_case_name = request.json.get('test_case_name')
    result = request.json.get('result')
    execution_date = request.json.get('date')

    # Check if the test asset exists
    cursor.execute('SELECT * FROM TestAssets WHERE name = ?', (test_asset_name,))
    test_asset = cursor.fetchone()

    if test_asset is None:
        return jsonify({'error': 'Test asset not found'}), 404
 # Check if the test case exists
    cursor.execute('SELECT * FROM TestCases WHERE name = ?', (test_case_name,))
    test_case = cursor.fetchone()

    if test_case is None:
        return jsonify({'error': 'Test case not found'}), 404

    # Insert the execution result into the ExecutionResults table
    cursor.execute('''
        INSERT INTO ExecutionResults (testCaseId, result, executionDate)
        VALUES (?, ?, ?)
    ''', ( test_case[0], result, execution_date))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return jsonify({'message': 'Execution result recorded successfully'}), 201

@app.route('/executionresults/<test_asset_name>', methods=['GET'])
def get_execution_results_by_test_asset(test_asset_name):
    conn = db_connection()
    cursor = conn.cursor()

    # Retrieve the execution results for the specific test asset
    cursor.execute('''
        SELECT er.executionDate, ta.name AS testAssetName, tc.name AS testCaseName, er.result
        FROM ExecutionResults er
        JOIN TestAssets ta ON tc.testAssetId = ta.id
        JOIN TestCases tc ON er.testCaseId = tc.id
        WHERE ta.name = ?
    ''', (test_asset_name,))

    results = cursor.fetchall()

    # Format the execution results as a list of dictionaries
    execution_results = []
    for row in results:
        execution_date = row[0]
        test_asset_name = row[1]
        test_case_name = row[2]
        result = row[3]

        execution_results.append({
            'execution_date': execution_date,
            'test_asset_name': test_asset_name,
            'test_case_name': test_case_name,
            'result': result
        })

    # Close the connection
    conn.close()

    return jsonify(execution_results), 200

@app.route('/')
def index():
    return 'Hello World'


if __name__ == '__main__':
    app.run()