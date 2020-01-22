#from django.http import HttpResponse
#from django.template import loader
#from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import BookingSeason, RoomType, RoomDescription, SeasonRoomPrice, RoomBooking, SeasonBookingCalendar


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
