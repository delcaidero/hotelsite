from django.urls import path
from . import views

urlpatterns = [
    path('', views.RoomBookingListView.as_view(), name='bookings'),
    path(r'(?P<pk>\d+)$', views.RoomBookingDetailView.as_view(), name='booking-detail'),
    path('<int:season_id>/add/', views.add_booking, name='booking-add'),
]