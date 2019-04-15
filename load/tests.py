from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from users.models import Shipper, Carrier
import datetime
from collections import OrderedDict


# Create your tests here.

class ShipperAPITestCase(APITestCase):
    url = reverse("load:shipper-list")
    client = APIClient()

    def setUp(self):
        self.user = Shipper.objects.create_user(
            email="hireme@loadsmart.com", password="iwilldoagreatjob")
        self.client.login(email="hireme@loadsmart.com",
                          password="iwilldoagreatjob")
        self.data_ = {
            "pickup_date": datetime.date(2019, 4, 11),
            "ref": "963",
            "origin_city": "Salvador",
            "destination_city": "Lauro de Freitas",
            "price": 75
        }
        self.client.post(self.url, self.data_, format="json")
        self.data_ = {
            "pickup_date": datetime.date(2019, 4, 11),
            "ref": "132",
            "origin_city": "Alagoinhas",
            "destination_city": "Feira de Santana",
            "price": 150
        }
        self.client.post(self.url, self.data_, format="json")

    def test_create_load(self):
        response = self.client.post(self.url, self.data_, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_available_loads(self):
        response = self.client.get(
            reverse("load:shipper-available"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_accepted_loads(self):
        response = self.client.get(
            reverse("load:shipper-accepted"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class CarrierAPITestCase(APITestCase):
    url = reverse("load:shipper-list")
    client = APIClient()

    def setUp(self):
        self.user = Shipper.objects.create_user(
            email="hireme@loadsmart.com", password="iwilldoagreatjob")
        self.user = Carrier.objects.update_or_create(user=self.user, mc_number="123456789")
        self.client.login(email="hireme@loadsmart.com",
                          password="iwilldoagreatjob")
        self.data_ = {
            "pickup_date": datetime.date(2019, 4, 11),
            "ref": "963",
            "origin_city": "Salvador",
            "destination_city": "Lauro de Freitas",
            "price": 75
        }
        self.client.post(self.url, self.data_, format="json")
        self.data_ = {
            "pickup_date": datetime.date(2019, 4, 11),
            "ref": "132",
            "origin_city": "Alagoinhas",
            "destination_city": "Feira de Santana",
            "price": 150
        }
        self.client.post(self.url, self.data_, format="json")

        self.data_ = {
            "pickup_date": datetime.date(2019, 4, 11),
            "ref": "132",
            "origin_city": "NY",
            "destination_city": "Los Angeles",
            "price": 1500
        }
        self.client.post(self.url, self.data_, format="json")
        self.client.get('/load/api/carrier/2/accept/', format="json")

    def test_accept_load(self):
        response = self.client.get(
            '/load/api/carrier/1/accept/', format="json")
        data_ = {
            "shipper": OrderedDict([('first_name', ''), ('last_name', ''), ('email', 'hireme@loadsmart.com')]),
            "carrier": 1,
            "pickup_date": '2019-04-11',
            "ref": "963",
            "origin_city": "Salvador",
            "destination_city": "Lauro de Freitas",
            "price": 75.0
        }
        self.assertEqual(response.data, data_)

    def test_accepted_load(self):
        response = self.client.get(
            '/load/api/carrier/accepted/', format="json")
        self.assertEqual(len(response.data), 1)

    def test_available_load(self):
        response = self.client.get(
            '/load/api/carrier/available/', format="json")
        self.assertEqual(len(response.data), 2)

    def test_drop_load(self):
        pass

    def test_list_dropped(self):
        pass
