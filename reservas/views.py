from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import AddBookingForm, AddBookingModelForm

from .models import BookingSeason, RoomType, RoomDescription, SeasonRoomPrice, RoomBooking, SeasonBookingCalendar, Robot


def index(request):
    season = BookingSeason.objects.get(pk=5)
    num_bookings = RoomBooking.objects.all().count()

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'reservas/index.html',
        context={'num_bookings': num_bookings, 'season': season},
    )


class RoomBookingListView(generic.ListView):
    model = RoomBooking
    context_object_name = 'booking_list'
    template_name = 'reservas/booking_list.html'

    def get_context_data(self, **kwargs):
        season = BookingSeason.objects.get(pk=5)
        # Call the base implementation first to get a context
        context = super(RoomBookingListView, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['season_url'] = season.get_add_booking_url()
        return context


class RoomBookingDetailView(generic.DetailView):
    model = RoomBooking
    template_name = 'reservas/booking_detail.html'


''' vistas para formularios'''

def add_booking(request, season_id):
    season = get_object_or_404(BookingSeason, pk=season_id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        form = AddBookingModelForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)
            booking.booking_season_id = season_id
            booking.check_in_date = form.cleaned_data['check_in_date']
            booking.check_out_date = form.cleaned_data['check_out_date']
            booking.room_type = form.cleaned_data['room_type']
            booking.pax = form.cleaned_data["pax"]
            booking.booking_localizator = Robot().name
            booking.booking_date = datetime.date.today()
            booking.booking_price = booking.get_total_price()

            if not booking.is_available():
                form.add_error('room_type','Room type not available for booking dates')
                return render(request, 'reservas/booking_add.html', {'form': form, 'season': season})

            booking.save()
            booking.set_calendar_dates()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('bookings') )

    else:
        proposed_check_in_date = datetime.date.today()
        proposed_check_out_date = datetime.date.today() + datetime.timedelta(days=1)
        form = AddBookingModelForm(initial={'check_in_date': proposed_check_in_date,
                                            'check_out_date': proposed_check_out_date,
                                            })

    return render(request, 'reservas/booking_add.html', {'form': form, 'season':season})
