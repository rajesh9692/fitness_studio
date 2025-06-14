from django.test import TestCase, Client
from .models import FitnessClass, Booking
from django.utils import timezone as dj_tz
import json

class BookingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.cls = FitnessClass.objects.create(
            name="Yoga",
            date_time=dj_tz.now(),
            instructor="MR Sam",
            available_slots=5
        )

    def test_booking_reduces_slot(self):
        response = self.client.post('/book/', data=json.dumps({
            "class_id": self.cls.id,
            "client_name": "Dipti",
            "client_email": "diptir2000@gmail.com"
        }), content_type="application/json")

        self.cls.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cls.available_slots, 4)  # 5 - 1 = 4
