from django.test import TestCase
from django.urls import reverse

# Teste le formulaire de création d'une réservation
class ViewsTestCase(TestCase):
    def test_ajax(self):
        response = self.client.post(
            reverse('reservation_ajax'),
            data={'title': 'Titre',
                  'start_date': '2021-12-01 15:00:00',
                  'end_date': '2021-12-01 15:00:00',
                  'resource': 'Salle de réunion 2',
                  'user': 1
                  },
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
