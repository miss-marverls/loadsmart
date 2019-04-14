from django.test import TestCase
from django.urls import reverse
from .models import Shipper, Carrier

# Create your tests here.


class LogInViewTests(TestCase):

    def setUp(self):
        self.data_ = {
            'email': 'hireme_shipper@loadsmart.com',
            'password': 'iwilldoagreatjob'}
        self.user = Shipper.objects.create_user(**self.data_)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('users:login'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users:login'))
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login(self):
        response = self.client.post(reverse('users:login'), self.data_, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.login(
            username="hireme_shipper@loadsmart.com", password="iwilldoagreatjob"))
        


class RegisterViewTests(TestCase):

    def setUp(self):
        # Create a shipper user
        self.data_invalid = {
            'email': 'hireme@loadsmart.com',
            'password': 'iwilldoagreatjob'}

        self.data_shipper = {
            'first_name': 'hireme',
            'last_name': 'shipper',
            'email': 'hireme_shipper@loadsmart.com',
            'password': 'iwilldoagreatjob'}

        self.data_carrier = {
            'first_name': 'hireme',
            'last_name': 'carrier',
            'mc_number': '123456',
            'email': 'hireme_carrier@loadsmart.com',
            'password1': 'iwilldoagreatjob',
            'password2': 'iwilldoagreatjob'}
    
    def test_register_shipper(self):
        response = self.client.post(reverse('users:register_shipper'), self.data_invalid, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_register_carrier(self):
        response = self.client.post(reverse('users:register_carrier'), self.data_carrier, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertRedirects(response,reverse('users:login'))
        self.assertEqual(len(Carrier.objects.all()),1)

        


        

    

