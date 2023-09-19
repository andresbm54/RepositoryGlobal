import unittest
import json
from flask import Flask
from app import app, init_db

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        init_db()

    def test_home(self):
        response = self.app.get('/')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Welcome to the Globant Challenge API")

    def test_upload_csv(self):
        with open('departments.csv', 'rb') as csv_file:
            response = self.app.post('/upload_csv', 
                                     data={'csv_file': (csv_file, 'departments.csv'),
                                           'table_name': 'departments'},
                                     content_type='multipart/form-data')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["message"], "departments CSV uploaded and data inserted into DB")

    def test_insert_batch(self):
        data = [{'id': 1, 'department': 'Test'}]
        response = self.app.post('/insert_batch',
                                 json={'data': data,
                                       'table_name': 'departments'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["message"], "Batch inserted")

    def test_metric1(self):
        response = self.app.get('/metric1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        # Add assertions to verify specific data in the response
        # Use known data for this test

    def test_metric2(self):
        response = self.app.get('/metric2')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        # Add assertions to verify specific data in the response
        # Use known data for this test

    def test_insert_batch_limit(self):
        # Trying to insert more than 1000 records
        data = [{'id': i, 'department': f'Test{i}'} for i in range(1001)]
        response = self.app.post('/insert_batch',
                                 json={'data': data,
                                       'table_name': 'departments'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Cannot insert more than 1000 rows in a single request")

if __name__ == '__main__':
    unittest.main()
