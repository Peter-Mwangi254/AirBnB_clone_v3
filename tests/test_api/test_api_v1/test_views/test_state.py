#!/usr/bin/python3
'''Testing index.py view blueprint'''
import unittest
from unittest.mock import patch
import pytest
from api.v1.app import app
from api.v1.views import app_views
from api.v1.views.states import *


class TestState(unittest.TestCase):
    '''Testing state objects'''

    @patch('api.v1.views.states.storage')
    def test_get_states(self, mock_storage):
        '''test State objects retrieval'''
        mock_storage.all(State).return_value = 5
        with app.test_client()as client:
            response = client.get('/api/v1/states')
            self.assertEqual(response.status_code, 200)



if __name__ == "__main__":
    unittest.main()
