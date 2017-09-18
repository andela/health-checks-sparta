from django.test import TestCase

from hc.lib.telegram import get_user_id


class TelegramTestCase(TestCase):

    def test_get_user_id_works(self):
        data = {'result': [{'message': {'from': {'id': 762455, 'first_name': 'john', 'last_name': 'doe', 'username': 'jdoe'}}}]}
        assert get_user_id(data, 'jdoe') == 762455

    def test_get_width_returns_none(self):
        data = {'result': [{'message': {'from': {'id': 762455, 'first_name': 'john', 'last_name': 'doe', 'username': 'jdoe'}}}]}
        assert get_user_id(data, 'jb') == None
