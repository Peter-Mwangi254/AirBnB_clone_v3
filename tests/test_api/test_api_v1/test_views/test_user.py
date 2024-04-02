#!/usr/bin/python3
'''Testing index.py view blueprint'''
import unittest
from unittest.mock import patch
import pytest
from api.v1.app import app
from api.v1.views import app_views
from api.v1.views.users import *


class TestUser(unittest.TestCase):
    '''Testing User views(blueprints and routes'''

    @patch('api.v1.views.users.storage')
    def test_get_users(self, mock_storage):
        '''Testing retrieval of user objects'''
        mock_storage.get.return_value = ['Baba', 'Mama']
        with app.test_client() as client:
            response = client.get('/api/v1/users')
            self.assertEqual(response.status_code, 200)
            #self.assertEqual(response.json, ['Baba', 'Mama'])


if __name__ == '__main__':
    unittest.main()
