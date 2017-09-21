from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch
from datetime import timedelta as td
from django.core import mail


class SendAlertsTestCase(BaseTestCase):

    def setUp(self):
        super(SendAlertsTestCase, self).setUp()
        self.now = timezone.now()
        self.check = Check(user=self.alice, name="demo", status="up",
                           escalation_enabled = True,
                           escalation_list = "test@mail.com")
    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_handles_few(self, mock):
        yesterday = self.now - timedelta(days=1)
        names = ["Check %d" % d for d in range(0, 10)]

        for name in names:
            check = Check(user=self.alice, name=name)
            check.alert_after = yesterday
            check.status = "up"
            check.last_ping = timezone.now()
            check.save()

        result = Command().handle_many()
        self.assertTrue(result)

        handled_names = []
        for args, kwargs in mock.call_args_list:
            handled_names.append(args[0].name)

        self.assertSetEqual(set(names), set(handled_names))

    def test_it_handles_grace_period(self):
        # 1 day 30 minutes after ping the check is in grace period:
        self.check.last_ping = self.now - timedelta(days=1, minutes=30)
        self.check.save()

        # Expect no exceptions--
        response = Command().handle_one(self.check)
        self.assertTrue(response)

    def test_it_sends_escalations_down(self):
        self.check.last_ping = self.now
        self.check.escalation_time = self.now - td(hours=1)
        self.check.save()
        Command().handle_many()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Escalation: demo is down')

    def test_it_sends_escalations_up(self):
        self.check.last_ping = self.now
        self.check.escalation_up = False
        self.check.escalation_time = self.now - td(hours=1)
        self.check.save()
        Command().handle_many()
        self.assertEqual(len(mail.outbox), 1)
