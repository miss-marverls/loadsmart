from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from users.models import User, Shipper, Carrier
from .models import Load
from .forms import LoadForm
from rest_framework.authtoken.models import Token
import datetime
from collections import OrderedDict


# Create your tests here.

class ShipperAppTestCase(TestCase):
    fixtures = ['loads_views_testdata.json', 'users_views_testdata.json']

    def setUp(self):
        self.client.login(username="hireme@loadsmart.com", password="iwilldoagreatjob")

    def create_load(self):
        return Load(pickup_date=datetime.date.today(), ref="123", origin_city="NY", destination_city="Los Angeles",
                    shipper_price=1000)

    def test_create_load(self):
        load = self.create_load()
        self.assertTrue(isinstance(load, Load))
        self.assertEqual(load.__str__(), "123")

    def test_valid_form(self):
        data = {
            "pickup_date": datetime.date.today(),
            "ref": "132",
            "origin_city": "Alagoinhas",
            "destination_city": "Feira de Santana",
            "shipper_price": 150
        }
        form = LoadForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "pickup_date": datetime.date.today(),
            "ref": "132",
            "origin_city": "Alagoinhas",
            "shipper_price": 150
        }
        form = LoadForm(data=data)
        self.assertFalse(form.is_valid())

    def test_add_load(self):
        response = self.client.post(reverse('load:create-load'), {
            "pickup_date": datetime.date.today(),
            "ref": "132",
            "origin_city": "Alagoinhas",
            "destination_city": "Feira de Santana",
            "shipper_price": 100})
        self.assertEqual(response.status_code, 302)
        load = Load.objects.get(pk=17)
        self.assertEqual(load.carrier_price, 95)

    def test_update_load(self):
        response = self.client.post('/1/update/', {"shipper_price": 200})
        self.assertEqual(response.status_code, 302)
        load = Load.objects.get(pk=1)
        self.assertEqual(load.shipper_price, 200)
        self.assertEqual(load.carrier_price, 190)

    def test_load_list(self):
        response = self.client.get('/loads/')
        self.assertEqual(response.status_code, 200)

    def test_form_edit_price(self):
        resp = self.client.post('/1/update/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form']['shipper_price'].errors, [u'This field is required.'])


class CarrierAppTestCase(TestCase):
    fixtures = ['loads_views_testdata.json', 'users_views_testdata.json']

    def setUp(self):
        self.client.login(username="carrier@loadsmart.com", password="iwilldoagreatjob")

    def test_list_loads(self):
        response = self.client.get('/loads/')
        self.assertEqual(response.status_code, 200)

    def test_accept_load(self):
        response = self.client.get('/5/accept/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Load.objects.get(pk=5).carrier_id, 1)

    def test_accept_accepted_load(self):
        response = self.client.get('/1/accept/')
        self.assertEqual(response.status_code, 404)

    def test_drop_load(self):
        response = self.client.get('/5/drop/')
        load = Load.objects.get(pk=5)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Carrier.objects.get(pk=1) in load.dropped_by.all())

    def test_drop_accepted_load(self):
        response = self.client.get('/1/drop/')
        self.assertEqual(response.status_code, 404)


class ShipperAPITestCase(APITestCase):
    url = reverse("load:api-list")
    client = APIClient()

    def setUp(self):
        self.user = User.objects.create_user(
            email="hireme@loadsmart.com", password="iwilldoagreatjob", is_shipper="1")
        self.token = Token.objects.create(user=self.user)
        self.user = Shipper.objects.update_or_create(user=self.user)
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

    def test_create_invalid_load(self):
        response = self.client.post(self.url, data={
            "pickup_date": datetime.date.today(),
            "ref": "132",
            "origin_city": "Alagoinhas",
            "shipper_price": 150
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_unauthorized_method(self):
        response = self.client.delete('/api/loads/3/')
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})


class CarrierAPITestCase(APITestCase):
    url = reverse("load:api-list")
    client = APIClient()

    def setUp(self):
        self.user = User.objects.create_user(
            email="hireme@loadsmart.com", password="iwilldoagreatjob", is_shipper="1")
        self.token = Token.objects.create(user=self.user)
        self.user = Shipper.objects.update_or_create(user=self.user)
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
        self.user = User.objects.create_user(
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
            "shipper": OrderedDict(),
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

    def test_null_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get(
            '/api/loads/rejected/', format="json")
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})
