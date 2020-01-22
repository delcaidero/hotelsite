from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'^$', views.index, name='index'),
    path('bookings/', views.RoomBookingListView.as_view(), name='bookings'),
    path(r'(?P<pk>\d+)$', views.RoomBookingDetailView.as_view(), name='booking-detail'),
    #path('<int:room_booking_id>/', views.RoomBookingDetailView.as_view(), name='booking-detail'),
# ex: /polls/5/
    path('<int:season_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]