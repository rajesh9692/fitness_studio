from django.test import TestCase
from .models import FitnessClass, Booking
from django.utils import timezone as dj_tz

class BookingTestCase(TestCase):
    def test_booking_reduces_slot(self):
        cls = FitnessClass.objects.create(
            name="Yoga",
            date_time=dj_tz.now(),
            instructor="A",
            available_slots=1
        )
        Booking.objects.create(
            fitness_class=cls,
            client_name="Raj",
            client_email="raj@example.com"
        )
        cls.available_slots -= 1
        cls.save()
        cls.refresh_from_db()
        self.assertEqual(cls.available_slots, 0)
