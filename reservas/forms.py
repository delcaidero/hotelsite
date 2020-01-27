from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from .models import RoomBooking, RoomType


import datetime


class AddBookingForm(forms.Form):
    check_in_date = forms.DateField(help_text="Enter a Check in date.")


class AddBookingModelForm(ModelForm):

    def clean_check_in_date(self):
        data = self.cleaned_data['check_in_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - check-in in past'))

        # Check date is in range .
        if data > datetime.date(2020, 12, 31):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

    def clean_check_out_date(self):
        check_in = self.cleaned_data['check_in_date']
        check_out = self.cleaned_data['check_out_date']

        if check_out < datetime.date.today():
            raise ValidationError(_('Invalid date - check-out in past'))

        if check_in >= check_out:
            raise ValidationError(_('Invalid date - check-out before check-in'))

        # Remember to always return the cleaned data.
        return check_out

#    def clean_room_type(self):
#        type_data = self.cleaned_data['room_type']
#        return type_data

    def room_type_not_available(self):
            raise ValidationError(_('Room type not available for booking dates'))


    def clean_pax(self):
        type = self.cleaned_data['room_type']
        pax = int(self.cleaned_data['pax'])

        if type.room_type_max_pax < pax:
            raise ValidationError(_('Room type too small'))

        return pax

    class Meta:
        model = RoomBooking
        fields = ['check_in_date','check_out_date','room_type','room','pax','contact_name','contact_email','contact_phone','booking_comments']
        labels = {'check_in_date': _('Entrada'),
                  'check_out_date': _('Salida'),
                  'room_type': _('Tipo Hab.'),
                  'room': _('Num. Hab.'),
                  'pax': _('Huéspedes'),
                  'contact_name': _('Nombre'),
                  'contact_email': _('e-mail'),
                  'contact_phone': _('Teléfono'),
                  'booking_price': _('Total reserva'),
                  'booking_comments': _('Observaciones'),
                  }
        #help_texts = {'check_in_date': _('Enter a date between now and 4 weeks (default 3).'), }
