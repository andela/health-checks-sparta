from django.test import Client, TestCase

from hc.api.models import Check, Ping


class PingTestCase(TestCase):

    def setUp(self):
        super(PingTestCase, self).setUp()
        self.check = Check.objects.create()

    def test_it_works(self):
        r = self.client.get("/ping/%s/" % self.check.code)
        self.assertEqual(r.status_code, 200)

        self.check.refresh_from_db()
        self.assertEqual(self.check.status, "up")

        ping = Ping.objects.latest("id")
        self.assertEqual(ping.scheme, "http")

    def test_it_handles_bad_uuid(self):
        r = self.client.get("/ping/not-uuid/")
        self.assertEqual(r.status_code, 400)

    def test_it_handles_120_char_ua(self):
        ua = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/44.0.2403.89 Safari/537.36")

        r = self.client.get("/ping/%s/" % self.check.code, HTTP_USER_AGENT=ua)
        self.assertEqual(r.status_code, 200)

        ping = Ping.objects.latest("id")
        self.assertEqual(ping.ua, ua)

    def test_it_truncates_long_ua(self):
        ua = "01234567890" * 30

        r = self.client.get("/ping/%s/" % self.check.code, HTTP_USER_AGENT=ua)
        self.assertEqual(r.status_code, 200)

        ping = Ping.objects.latest("id")
        self.assertEqual(len(ping.ua), 200)
        self.assertTrue(ua.startswith(ping.ua))

    def test_it_reads_forwarded_ip(self):
        ip = "1.1.1.1"
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_FOR=ip)
        ping = Ping.objects.latest("id")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(ping.remote_addr, ip)

        ip = "1.1.1.1, 2.2.2.2"
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_FOR=ip, REMOTE_ADDR="3.3.3.3")
        ping = Ping.objects.latest("id")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(ping.remote_addr, "1.1.1.1")

    def test_it_reads_forwarded_protocol(self):
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_PROTO="https")
        ping = Ping.objects.latest("id")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(ping.scheme, "https")

    def test_it_never_caches(self):
        r = self.client.get("/ping/%s/" % self.check.code)
        assert "no-cache" in r.get("Cache-Control")

    def test_it_works_with_post(self):
        r = self.client.post("/ping/%s/" % self.check.code)
        self.assertEqual(r.status_code, 200)
        self.check.refresh_from_db()
        self.assertEqual(self.check.status, "up")
        ping = Ping.objects.latest("id")
        self.assertEqual(ping.scheme, "http")

    def test_it_changes_status(self):
        self.check.status = "paused"
        self.check.save()
        r = self.client.get("/ping/%s/" % self.check.code)
        self.assertEqual(r.status_code, 200)
        self.check.refresh_from_db()
        self.assertEqual(self.check.status, "up")

    def test_csrf_client_works(self):
        client = Client(enforce_csrf_checks=True)
        r = client.get("/ping/%s/" % self.check.code)
        self.assertEqual(r.status_code, 200)
