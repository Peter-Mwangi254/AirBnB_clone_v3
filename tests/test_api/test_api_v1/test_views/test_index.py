#!/usr/bin/python3
'''Testing index.py view blueprint'''
import unittest
from unittest.mock import patch
import pytest
from api.v1.app import app
from api.v1.views import app_views
from api.v1.views.index import *


class TestIndex(unittest.TestCase):
    '''Testing of our index.py routes'''

    def SetUp(self):
        '''Tests setup of flask server'''
        self.app = app
        self.app.register_blueprint(app_views)
        self.app.testing = True
        self.client = self.app.test_client()

    def test_status(self):
        '''Test when status is successful'''
        with app.test_client() as client:
            response = client.get('/api/v1/status')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"status": "OK"})


    @patch('api.v1.views.index.storage')
    def test_get_data(self, mock_storage):
        '''tests get_total method that gets total insts of a class'''
        mock_storage.count.return_value = 5
        with app.test_client() as client:
            response = client.get('/api/v1/stats')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json,
                             { "amenities": 5,
                               "cities": 5,
                               "places":5,
                               "reviews": 5,
                               "states": 5,
                               "users": 5})


if __name__ == "__main__":
    unittest.main()
