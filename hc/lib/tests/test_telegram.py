import requests, json, os
from requests.models import Response
from django.test import TestCase

from hc.lib.telegram import get_user_id, get_telegram_id
import mock

class TelegramTestCase(TestCase):

    def setUp(self):
        self.data = {'result': [{'message': {'from': {'id': 762455, 'first_name': 'john', 'last_name': 'doe', 'username': 'jdoe'}}}]}
        
    def test_get_user_id_works(self):
        assert get_user_id(self.data, 'jdoe') == 762455

    def test_get_width_returns_none(self):
        assert get_user_id(self.data, 'jb') == None

    def test_get_telegram_id(self):
        response = Response()
        response.status_code = 200
        response.json = lambda : self.data

        mocked_get = mock.MagicMock(return_value=response)

        with mock.patch('requests.get', mocked_get):
            r = get_telegram_id('jdoe')
            self.assertEquals(762455, r)
            self.assertIsNone(get_telegram_id('invalid_username'))
        
