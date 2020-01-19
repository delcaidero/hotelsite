import datetime
from django.db import models


class BookingSeason(models.Model):
    season_text = models.CharField(max_length=200)
    start_check_in_date = models.DateTimeField('Check in date')
    end_check_out_date = models.DateTimeField('Check out date')

    def __str__(self):
        return self.season_text


class RoomType(models.Model):
    room_type_text = models.CharField(max_length=200)
    room_type_max_pax = models.IntegerField(default=0)

    def __str__(self):
        return self.room_type_text


class RoomDescription(models.Model):
    room_number_text = models.CharField(max_length=3)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)

    def __str__(self):
        return self.room_number_text


class SeasonRoomPrice(models.Model):
    booking_season = models.ForeignKey(BookingSeason, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_type_price = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)


class RoomBooking(models.Model):
    check_in_date = models.DateTimeField('Check in date')
    check_out_date = models.DateTimeField('Check out date')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    pax = models.IntegerField(default=0)
    contact_name = models.CharField(max_length=200)
    contact_email = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=20)
    booking_date = models.DateTimeField('Booking date')
    booking_price = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    booking_comments = models.CharField(max_length=200)
    booking_localizator = models.CharField(max_length=6)


class SeasonBookingCalendar(models.Model):
    date = models.DateTimeField('Check in date')
    check_in = models.BooleanField()
    check_out = models.BooleanField()
    room_booking = models.ForeignKey(RoomBooking, on_delete=models.CASCADE)