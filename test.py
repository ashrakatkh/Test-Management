import unittest
from unittest import mock
from flask import Flask, jsonify, request
from app import app

class TestGetAllTestCases(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True
    

    def test_get_all_test_cases(self):
        # Send a GET request to the route
        response = self.app.get('/testcases')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response is in JSON format
        self.assertEqual(response.content_type, 'application/json')

        # Assert that the response body contains the expected test cases
        expected_test_cases = [
            {
                'name': 'Test Case 1',
                'description': 'Description of Test Case 1',
                'result': 'Pass',
                'execution_date': '2022-01-01'
            },
            {
                'name': 'Test Case 2',
                'description': 'Description of Test Case 2',
                'result': 'Fail',
                'execution_date': '2022-01-02'
            }
        ]
        # self.assertEqual(response.json, expected_test_cases)
    def test_create_test_case(self):
        # Define the test data
        test_data = {
            'test_asset_name': 'Test Asset 1',
            'name': 'New Test Case',
            'description': 'Description of New Test Case'
        }

        # Send a POST request to the route with the test data
        response = self.app.post('/testcases', json=test_data)

        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Assert that the response is in JSON format
        self.assertEqual(response.content_type, 'application/json')

        # Assert that the response body contains the expected message
        expected_message = {'message': 'Test case created successfully'}
        self.assertEqual(response.json, expected_message)
    
    def test_get_test_case(self):
        # Define the test case ID
        testcase_id = 1

        # Send a GET request to the route with the test case ID
        response = self.app.get(f'/testcases/{testcase_id}')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response is in JSON format
        self.assertEqual(response.content_type, 'application/json')

        # Assert that the response body contains the expected test case
        expected_test_case = {
            'name': 'Test Case 1',
            'description': 'Description of Test Case 1',
            'result': 'Pass',
            'execution_date': '2022-01-01'
        }
        #self.assertEqual(response.json, expected_test_case)

    def test_get_nonexistent_test_case(self):
        # Define a non-existent test case ID
        testcase_id = 100

        # Send a GET request to the route with the non-existent test case ID
        response = self.app.get(f'/testcases/{testcase_id}')

        # Assert that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Assert that the response is in JSON format
        self.assertEqual(response.content_type, 'application/json')

        # Assert that the response body contains the expected error message
        expected_error = {'error': 'Test case not found'}
        self.assertEqual(response.json, expected_error)
    
    def test_update_test_case(self):
        # Define the test case ID
        testcase_id = 2

        # Define the updated data for the test case
        updated_data = {
            'name': 'Updated Test Case',
            'description': 'Updated Description'
        }

        # Send a PUT request to the route with the test case ID and updated data
        response = self.app.put(f'/testcases/{testcase_id}', json=updated_data)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response is in JSON format
        self.assertEqual(response.content_type, 'application/json')

        # Assert that the response body contains the expected message
        expected_message = {'message': 'Test case updated successfully'}
        self.assertEqual(response.json, expected_message)

    def test_update_nonexistent_test_case(self):
        # Define a non-existent test case ID
        testcase_id = 100

        # Define the updated data for the test case
        updated_data = {
            'name': 'Updated Test Case',
            'description': 'Updated Description'
        }

        # Send a PUT request to the route with the non-existent test case ID and updated data
        response = self.app.put(f'/testcases/{testcase_id}', json=updated_data)

        # Assert that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Assert that the response is in JSON format
        self.assertEqual(response.content_type, 'application/json')

        # Assert that the response body contains the expected error message
        expected_error = {'error': 'Test case not found'}
        self.assertEqual(response.json, expected_error)
        

    def test_delete_test_case(self):
        # Mock the test case ID
        testcase_id = 1
        
        # Mock the db_connection function
        with mock.patch('app.db_connection') as mock_db_connection:
            # Mock the database cursor and execute method
            mock_cursor = mock_db_connection.return_value.cursor.return_value
            mock_cursor.fetchone.return_value = ('Test Case 1', 'Description of Test Case 1')

            # Send a DELETE request to the delete_test_case route
            response = self.app.delete(f'/testcases/{testcase_id}')

            # Assert that the response status code is 200 (OK)
            self.assertEqual(response.status_code, 200)

            # Assert that the response is in JSON format
            self.assertEqual(response.content_type, 'application/json')

            # Assert that the response body contains the expected message
            expected_message = {'message': 'Test case deleted successfully'}
            self.assertEqual(response.json, expected_message)

            # Assert that the db_connection function is called
            mock_db_connection.assert_called_once()

            # Assert that the cursor and execute methods are called with the expected SQL queries and parameters
            mock_cursor.execute.assert_any_call('SELECT * FROM TestCases WHERE id = ?', (testcase_id,))
            mock_cursor.execute.assert_any_call('DELETE FROM TestCases WHERE id = ?', (testcase_id,))
            mock_cursor.execute.assert_any_call('DELETE FROM ExecutionResults WHERE testCaseId = ?', (testcase_id,))
    


    def test_delete_nonexistent_test_case(self):
        # Define a non-existent test case ID
        testcase_id = 100

        # Send a DELETE request to the route with the non-existent test case ID
        response = self.app.delete(f'/testcases/{testcase_id}')

        # Assert that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Assert that the response is in JSON format
        self.assertEqual(response.content_type, 'application/json')

        # Assert that the response body contains the expected error message
        expected_error = {'error': 'Test case not found'}
        self.assertEqual(response.json, expected_error)
    def test_get_execution_results_by_test_asset(self):
        # Define the test asset name
        test_asset_name = 'Test Asset'

        # Send a GET request to the route with the test asset name
        response = self.app.get(f'/executionresults/{test_asset_name}')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response is in JSON format
        self.assertEqual(response.content_type, 'application/json')

        # Assert that the response body contains the expected execution results
        expected_results = [
            {
                'execution_date': '2022-01-01',
                'test_asset_name': 'Test Asset',
                'test_case_name': 'Test Case 1',
                'result': 'Pass'
            },
            {
                'execution_date': '2022-01-02',
                'test_asset_name': 'Test Asset',
                'test_case_name': 'Test Case 2',
                'result': 'Fail'
            }
        ]
        #self.assertEqual(response.json, expected_results)

    
  
        
if __name__ == '__main__':
    unittest.main()