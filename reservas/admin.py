from django.contrib import admin

from .models import BookingSeason, RoomType, RoomDescription, SeasonRoomPrice, RoomBooking, SeasonBookingCalendar

#admin.site.register(BookingSeason)
admin.site.register(RoomType)
# admin.site.register(RoomDescription)
admin.site.register(SeasonRoomPrice)
# admin.site.register(RoomBooking)
admin.site.register(SeasonBookingCalendar)

class SeasonRoomPriceInline(admin.TabularInline):
    model = SeasonRoomPrice

@admin.register(BookingSeason)
class BookingSeasonAdmin(admin.ModelAdmin):
    list_display = ('season_text', 'start_check_in_date', 'end_check_out_date', 'display_room_bookings', 'display_nights_booked')
    inlines = [SeasonRoomPriceInline]

@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('check_in_date', 'check_out_date', 'room_type', 'booking_price', 'booking_localizator')
    list_filter = ('check_in_date', 'check_out_date', 'room_type')
    fieldsets = (
        (None, {
            'fields': ('check_in_date', 'check_out_date', 'room_type', 'pax')
        }),
        ('Contact', {
            'fields': ('contact_name', 'contact_email', 'contact_phone')
        }),
    )

@admin.register(RoomDescription)
class RoomDescriptionAdmin(admin.ModelAdmin):
    list_display = ('room_number_text', 'room_type')