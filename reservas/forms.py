from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.


class AddBookingForm(forms.Form):
    check_in_date = forms.DateField(help_text="Enter a Check in date.")

    def clean_check_in_date(self):
        data = self.cleaned_data['check_in_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

from django.forms import ModelForm
from .models import RoomBooking

class AddBookingModelForm(ModelForm):

    def clean_check_in_date(self):
        data = self.cleaned_data['check_in_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

    class Meta:
        model = RoomBooking
        fields = ['booking_season','check_in_date','check_out_date','room_type','pax','contact_name','contact_email','contact_phone','booking_date','booking_price','booking_comments','booking_localizator']
        labels = {'check_in_date': _('Renewal date'), }
        help_texts = {'check_in_date': _('Enter a date between now and 4 weeks (default 3).'), }
