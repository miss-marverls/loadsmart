from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from users.models import Shipper, Carrier
from rest_framework.authtoken.models import Token
import datetime
from collections import OrderedDict


# Create your tests here.

class ShipperAPITestCase(APITestCase):
    url = reverse("load:api-list")
    client = APIClient()

    def setUp(self):
        self.user = Shipper.objects.create_user(
            email="hireme@loadsmart.com", password="iwilldoagreatjob", is_shipper="1")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.data_ = {
            "pickup_date": datetime.date(2019, 4, 11),
            "ref": "963",
            "origin_city": "Salvador",
            "destination_city": "Lauro de Freitas",
            "shipper_price": 75
        }
        self.client.post(self.url, self.data_, format="json")
        self.data_ = {
            "pickup_date": datetime.date(2019, 4, 11),
            "ref": "132",
            "origin_city": "Alagoinhas",
            "destination_city": "Feira de Santana",
            "shipper_price": 150
        }
        self.client.post(self.url, self.data_, format="json")

    def test_create_load(self):
        response = self.client.post(self.url, self.data_, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_available_loads(self):
        response = self.client.get(
            reverse("load:api-available"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_accepted_loads(self):
        response = self.client.get(
            reverse("load:api-accepted"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class CarrierAPITestCase(APITestCase):
    url = reverse("load:api-list")
    client = APIClient()

    def setUp(self):
        self.user = Shipper.objects.create_user(
            email="hireme@loadsmart.com", password="iwilldoagreatjob", is_shipper="1")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.data_ = {
            "pickup_date": datetime.date(2019, 4, 11),
            "ref": "963",
            "origin_city": "Salvador",
            "destination_city": "Lauro de Freitas",
            "shipper_price": 75
        }
        self.client.post(self.url, self.data_, format="json")
        self.data_ = {
            "pickup_date": datetime.date(2019, 4, 11),
            "ref": "132",
            "origin_city": "Alagoinhas",
            "destination_city": "Feira de Santana",
            "shipper_price": 150
        }
        self.client.post(self.url, self.data_, format="json")

        self.data_ = {
            "pickup_date": datetime.date(2019, 4, 11),
            "ref": "132",
            "origin_city": "NY",
            "destination_city": "Los Angeles",
            "shipper_price": 1500
        }
        self.client.post(self.url, self.data_, format="json")
        self.client.logout()
        self.user = Shipper.objects.create_user(
            email="carrier@loadsmart.com", password="iwilldoagreatjob", is_carrier="1")
        self.token = Token.objects.create(user=self.user)
        self.user = Carrier.objects.update_or_create(user=self.user, mc_number="123456789")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.post('/api/loads/2/accept/', format="json")
        self.client.post('/api/loads/3/reject/', format="json")

    def test_accept_load(self):
        response = self.client.post(
            '/api/loads/1/accept/', format="json")
        data_ = {
            "shipper": OrderedDict([('first_name', ''), ('last_name', ''), ('email', 'hireme@loadsmart.com')]),
            "carrier": 1,
            "pickup_date": '2019-04-11',
            "ref": "963",
            "origin_city": "Salvador",
            "destination_city": "Lauro de Freitas",
            "carrier_price": 71.25
        }
        self.assertEqual(response.data, data_)

    def test_accept_invalid_load(self):
        response = self.client.post(
            '/api/loads/2/accept/', format="json")
        self.assertEqual(response.data, {
            "detail": "Not found."
        })

    def test_accepted_load(self):
        response = self.client.get(
            '/api/loads/accepted/', format="json")
        self.assertEqual(len(response.data), 1)

    def test_available_load(self):
        response = self.client.get(
            '/api/loads/available/', format="json")
        self.assertEqual(len(response.data), 1)

    def test_drop_load(self):
        response = self.client.post('/api/loads/1/reject/')
        self.assertEqual(response.data, status.HTTP_201_CREATED)

    def test_drop_load_invalid(self):
        response = self.client.post('/api/loads/3/reject/')
        self.assertEqual(response.data, {
            "detail": "Load already dropped"
        })

    def test_list_dropped(self):
        response = self.client.get(
            '/api/loads/rejected/', format="json")
        self.assertEqual(len(response.data), 1)
