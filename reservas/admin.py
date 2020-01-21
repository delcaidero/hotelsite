from django.contrib import admin

from .models import BookingSeason, RoomType, RoomDescription, SeasonRoomPrice, RoomBooking, SeasonBookingCalendar

admin.site.register(BookingSeason)
admin.site.register(RoomType)
admin.site.register(RoomDescription)
admin.site.register(SeasonRoomPrice)
admin.site.register(RoomBooking)
admin.site.register(SeasonBookingCalendar)
