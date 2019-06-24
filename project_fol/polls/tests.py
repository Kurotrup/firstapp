import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question


class QuestionModelTests(TestCase):
    def test_was_pub_res_with_future_q(self):
        """ was_pub_res() returns False for questions whose pub_date
        is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        f_q = Question(pub_date=time)
        self.assertIs(f_q.was_pud_res(), False)

    def test_was_pub_res_with_old_q(self):
        """ was_pub_res() returns False for questions whose pub_date
        is older the 1 day"""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        ol_q = Question(pub_date=time)
        self.assertIs(ol_q.was_pud_res(), False)

    def test_was_pub_res_with_res_q(self):
        """ was_pub_res() returns True for questions whose pub_date
        is within last day"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        res_q = Question(pub_date=time)
        self.assertIs(res_q.was_pud_res(), True)
