from django.test import TestCase
from django.contrib.auth.models import User
from App.models import Booking, Resource

# Teste l'enregistrement d'une réservation avec ses clés étrangères
class BookingTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(id=1, username="TestUser", password=12345)
        ressource1 = Resource.objects.create(id=1, label="Salle de réunion 1",
                                             type_resource="Salle de réunion",
                                             location="Étage 1",
                                             capacity=5)
        ressource2 = Resource.objects.create(id=2, label="Salle de réunion 2",
                                             type_resource="Salle de visioconférence",
                                             location="Étage 2",
                                             capacity=5)
        Booking.objects.create(id=1, title="Décembre", start_date="2021-12-01 15:00:00",
                               end_date="2021-12-01 15:05:00",
                               resource=ressource1, user=user1)
        Booking.objects.create(id=2, title="Octobre", start_date="2021-10-01 15:00:00",
                               end_date="2021-10-01 15:05:00",
                               resource=ressource2, user=user1)

    def test_booking_model(self):
        booking1 = Booking.objects.get(title="Octobre")
        booking2 = Booking.objects.get(title="Décembre")
        self.assertEqual(booking1.resource.label, "Salle de réunion 2")
        self.assertEqual(booking2.user.username, "TestUser")
