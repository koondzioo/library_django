import datetime

from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewalBookForm


class RenewBookFormTest(TestCase):

    def test_renew_form_date_field_label(self):
        form = RenewalBookForm()
        self.assertTrue(form.fields['renewal_date'].label == None or form.fields['renewal_date'].label == 'Przedłuż do')

    def test_renew_form_date_field_help_text(self):
        form = RenewalBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Wprowadz datę od teraz do maksymalnie 4 tygodni w przód (domyślnie 3)')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewalBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_in_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        # date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewalBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_in_max_2(self):
        date = timezone.localtime() + datetime.timedelta(weeks=5)
        # date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewalBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_today(self):
        date = datetime.date.today()
        form = RenewalBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
