#from django.http import HttpResponse
#from django.template import loader
#from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import BookingSeason


def index(request):
    latest_season_list = BookingSeason.objects.order_by('-start_check_in_date')[:5]
    context = {'latest_season_list': latest_season_list}
    return render(request, 'reservas/index.html', context)

def detail(request, season_id):
    season = get_object_or_404(BookingSeason, pk=season_id)
    return render(request, 'reservas/detail.html', {'season': season})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
