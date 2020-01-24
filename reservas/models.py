import datetime
from django.db import models
from django.urls import reverse
from django.utils import timezone
import random
import string


class Robot(object):

    def __init__(self):
        self.name = ''
        self.robotState = random.getstate()
        self.reset()

    def reset(self):
        random.setstate(self.robotState)
        alphabet = set(string.ascii_lowercase[:28])
        prefix = random.sample(alphabet, k=2)
        prefix = ''.join(str(e) for e in prefix).upper()
        number = random.sample(range(9), k=3)
        number = ''.join(str(e) for e in number)
        self.name = prefix + number
        self.robotState = random.getstate()


class BookingSeason(models.Model):
    season_text = models.CharField('Season title',max_length=200)
    start_check_in_date = models.DateTimeField('Season start')
    end_check_out_date = models.DateTimeField('Season ends')

    def __str__(self):
        return self.season_text

    def get_total_nights(self):
        periodo = self.end_check_out_date - self.start_check_in_date
        return periodo.days

    def get_total_rooms_type(self,type):
        return RoomDescription.objects.filter(room_type=type).count()

    def get_add_booking_url(self):
        return reverse('booking-add', args=[str(self.id)])

    get_add_booking_url.short_description = 'add_booking'

    def display_room_bookings(self):
        return self.roombooking_set.count()

    display_room_bookings.short_description = 'Bookings'

    def display_nights_booked(self):
        return sum([booking.get_nights() for booking in self.roombooking_set.all()])

    display_nights_booked.short_description = 'Nights booked'


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

    def __str__(self):
        return str(self.room_type_price) + '/' +str(self.room_type)


class RoomBooking(models.Model):
    booking_season = models.ForeignKey(BookingSeason, on_delete=models.CASCADE)
    check_in_date = models.DateField('Check in date')
    check_out_date = models.DateField('Check out date')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room = models.ForeignKey(RoomDescription, on_delete=models.SET_NULL, null=True)
    pax = models.IntegerField(default=1)
    contact_name = models.CharField(max_length=200)
    contact_email = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=20)
    booking_date = models.DateTimeField('Booking date')
    booking_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    booking_comments = models.CharField(max_length=200)
    booking_localizator = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.check_in_date} ({self.get_nights()} nights) ({self.room_type})'

    def get_nights(self):
        nights = self.check_out_date - self.check_in_date
        return nights.days

    def get_absolute_url(self):
        return reverse('booking-detail', args=[str(self.id)])

    def set_calendar_dates(self):
        self.seasonbookingcalendar_set.create(date=self.check_in_date, check_in=True)
        self.seasonbookingcalendar_set.create(date=self.check_out_date, check_out=True)
        i = 1
        while self.check_out_date > self.check_in_date + datetime.timedelta(days=i):
            booking_date = self.check_in_date + datetime.timedelta(days=i)
            self.seasonbookingcalendar_set.create(date=booking_date)
            i += 1

    def get_season_room_price(self):
        return SeasonRoomPrice.objects.filter(room_type=self.room_type_id)[0]

    def get_total_price(self):
        return float(self.get_season_room_price().room_type_price) * self.get_nights()


class SeasonBookingCalendar(models.Model):
    date = models.DateField()
    check_in = models.BooleanField(default=False)
    check_out = models.BooleanField(default=False)
    room_booking = models.ForeignKey(RoomBooking, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} ({self.room_booking_id})'
