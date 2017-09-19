import mock
from django.test.utils import override_settings
from requests.models import Response
from hc.api.models import Channel, User
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops", "sms", "telegram")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    ### Test that the team access works
    def test_team_access_works(self):
        url = "/integrations/add/"
        form = {"kind": "email"}

        # Logging in as bob, not alice. Bob has team access so this
        # should work.
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url, form)

        user_alice = User.objects.get(email="alice@example.org")
        user_charlie = User.objects.get(email="charlie@example.org")

        # Alice is on Bob's team so se should have one Channel
        assert Channel.objects.filter(user=user_alice).count() == 1

        # Charlie is not part of the team so he should have no Channel
        assert Channel.objects.filter(user=user_charlie).count() == 0
        
    ### Test that bad kinds don't work
    def test_bad_kinds_dont_work(self):
        url = "/integrations/add/"
        form = {"kind": "invalid_kind", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)
        assert r.status_code == 400
    
    def test_it_adds_telegram(self):
        url = "/integrations/add/"
        form = {"kind": "telegram", "value": "jdoe"}
        response = Response()
        response.status_code = 200
        response.json =  lambda: {'result': [{'message': {'from': {'id': 762455, 'first_name': 'john', 'last_name': 'doe', 'username': 'jdoe'}}}]}

        mocked_get = mock.MagicMock(return_value=response)

        with mock.patch('requests.get', mocked_get):

            self.client.login(username="alice@example.org", password="password")
            r = self.client.post(url, form)

            self.assertRedirects(r, "/integrations/")
            assert Channel.objects.count() == 1
    
    def test_it_redirects_on_invalid_telegram_username(self):
        url = "/integrations/add/"
        form = {"kind": "telegram", "value": "invalid"}
        response = Response()
        response.status_code = 200
        response.json = lambda: {'result': [{'message': {'from': {'id': 762455, 'first_name': 'john', 'last_name': 'doe', 'username': 'jdoe'}}}]}

        mocked_get = mock.MagicMock(return_value=response)

        with mock.patch('requests.get', mocked_get):

            self.client.login(username="alice@example.org", password="password")
            r = self.client.post(url, form)

            self.assertRedirects(r, "/integrations/add_telegram/?failed=1")
            assert Channel.objects.count() == 0
