#from django.http import HttpResponse
#from django.template import loader
#from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import BookingSeason, RoomType, RoomDescription, SeasonRoomPrice, RoomBooking, SeasonBookingCalendar, Robot


def index(request):
    #latest_season_list = BookingSeason.objects.order_by('-start_check_in_date')[:5]
    #context = {'latest_season_list': latest_season_list}
    #return render(request, 'reservas/index.html', context)
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_bookings = RoomBooking.objects.all().count()

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'reservas/index.html',
        context={'num_bookings': num_bookings},
    )

def detail(request, season_id):
    season = get_object_or_404(BookingSeason, pk=season_id)
    return render(request, 'reservas/detail.html', {'season': season})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


class RoomBookingListView(generic.ListView):
    model = RoomBooking
    context_object_name = 'booking_list'
    #queryset = Book.objects.filter(title__icontains='war')[:5]  # Get 5 books containing the title war
    template_name = 'reservas/booking_list.html'


class RoomBookingDetailView(generic.DetailView):
    model = RoomBooking
    template_name = 'reservas/booking_detail.html'

''' vistas para formularios'''

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse
from django.urls import reverse
import datetime

from .forms import AddBookingForm, AddBookingModelForm

def add_booking(request, season_id):
    #book_inst=get_object_or_404(BookInstance, pk = pk)
    season = get_object_or_404(BookingSeason, pk=season_id)
    #booking = season.roombooking_set.create(request.POST)


    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddBookingModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            booking = form.save(commit=False)
            booking.check_in_date = form.cleaned_data['check_in_date']
            booking.booking_localizator = Robot().name
            booking.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('bookings') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_check_in_date = datetime.date.today()
        #form = AddBookingForm(initial={'check_in_date': proposed_check_in_date,})
        form = AddBookingModelForm(initial={'check_in_date': proposed_check_in_date,})

    #return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
    return render(request, 'reservas/booking_add.html', {'form': form, 'season':season})


def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})