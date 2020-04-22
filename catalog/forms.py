import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import fields
from django.utils.translation import ugettext_lazy as _
from django import forms

from catalog.models import BookOrder


class RenewalBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Wprowadz datę od teraz do maksymalnie 4 tygodni w przód (domyślnie 3)")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Niepoprawna data - data sprzed dnia dzisiejszego.'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Niepoprawna data - wykracza poza dozwolone 4 tygodnie liczone od dziś.'))

        return data


class ChangeBookOrderStatusForm(forms.ModelForm):
    class Meta:
        model = BookOrder
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(ChangeBookOrderStatusForm, self).__init__(*args, **kwargs)
        status_choices = [('m', 'maintenance'), ('a', 'available')]
        self.fields['status'].choices = status_choices


class BookOrderForm(forms.ModelForm):

    class Meta:
        model = BookOrder
        fields = ['status', 'date_of_return', 'user']

    def __init__(self, *args, **kwargs):
        super(BookOrderForm, self).__init__(*args, **kwargs)
        user = kwargs['initial']['user']
        status_choices = [('o', 'on loan'), ('r', 'reserved')]

        self.fields['status'].choices = status_choices
        self.fields['user'].queryset = User.objects.filter(username=user)
        # self.fields['borrower'].empty_label = None # deleting  "-------" from choice list for borrower field

    def clean_due_back(self):
        due_back = self.cleaned_data["due_back"]
        # Check if a date is not in the past.
        if due_back < datetime.date.today():
            raise ValidationError(_('Niepoprawna data - data sprzed dnia dzisiejszego'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if due_back > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Niepoprawna data - wykracza poza dozwolone 4 tygodnie liczone od dziś.'))
        # Remember to always return the cleaned data.
        return due_back