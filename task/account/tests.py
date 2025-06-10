from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
import pytz
from .models import FitnessClass, Booking

class FitnessClassBookingTests(APITestCase):

    def setUp(self):
        # Create a fitness class with slots
        ist = pytz.timezone('Asia/Kolkata')
        dt_ist = ist.localize(timezone.datetime(2025, 6, 10, 8, 30))
        self.fitness_class = FitnessClass.objects.create(
            name="Morning Yoga",
            date_time=dt_ist.astimezone(pytz.UTC),
            instructor="Jane Doe",
            available_slots=3
        )

    def test_get_classes(self):
        url = reverse('fitnessclass-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Morning Yoga")

    def test_successful_booking(self):
        url = reverse('booking-create')
        data = {
            "fitness_class": self.fitness_class.id,
            "client_name": "Alice Johnson",
            "client_email": "alice@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 2)  # slots reduced by 1

    def test_overbooking(self):
        # Book all available slots
        for i in range(3):
            Booking.objects.create(
                fitness_class=self.fitness_class,
                client_name=f"Client{i}",
                client_email=f"client{i}@example.com"
            )
        self.fitness_class.available_slots = 0
        self.fitness_class.save()

        url = reverse('booking-create')
        data = {
            "fitness_class": self.fitness_class.id,
            "client_name": "Late Comer",
            "client_email": "late@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No slots available', str(response.data))

    def test_get_bookings_by_email(self):
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="Alice Johnson",
            client_email="alice@example.com"
        )
        url = reverse('booking-list') + '?email=alice@example.com'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['client_name'], "Alice Johnson")

    def test_get_bookings_no_email(self):
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)  # ValidationError triggered
