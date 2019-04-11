from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status


# Create your tests here.

class LoadCreateAPIViewTestCase(APITestCase):
    url = reverse("load:load-list")
    client = APIClient()

    def test_create_load(self):
        response = self.client.post(self.url, {
            "shipper": 3,
            "carrier": None,
            "pickup_date": "2019-05-04",
            "ref": "963",
            "origin_city": "Salvador",
            "destination_city": "Lauro de Freitas",
            "price": 75.0
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
