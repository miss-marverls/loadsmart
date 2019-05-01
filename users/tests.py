from django.test import TestCase
from django.urls import reverse

from .models import User


class LogInViewTests(TestCase):
    """
    Test class for the login views.
    """

    def setUp(self):
        self.data_ = {
            'email': 'hireme_shipper@loadsmart.com',
            'password': 'iwilldoagreatjob'}
        self.user = User.objects.create_user(**self.data_)

    def test_view_url_by_name(self):
        """
        Test if the login view name returns a valid response code.
        """

        response = self.client.get(reverse('users:login'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if the login view renders the correct template.
        """

        response = self.client.get(reverse('users:login'))
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login(self):
        """
        Test the login using email as username.
        """

        response = self.client.post(
            reverse('users:login'), self.data_, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.login(
            username="hireme_shipper@loadsmart.com", password="iwilldoagreatjob"))


class RegisterViewTests(TestCase):
    """
    Test class for the register views.
    """

    def setUp(self):
        # Create an invalid user
        self.data_invalid = {
            'email': 'hireme@loadsmart.com',
            'password': 'iwilldoagreatjob'}

        # Create a shipper
        self.data_shipper = {
            'first_name': 'hireme',
            'last_name': 'shipper',
            'email': 'hireme_shipper@loadsmart.com',
            'password1': 'iwilldoagreatjob',
            'password2': 'iwilldoagreatjob'}

        # Create a carrier
        self.data_carrier = {
            'first_name': 'hireme',
            'last_name': 'carrier',
            'mc_number': '123456',
            'email': 'hireme_carrier@loadsmart.com',
            'password1': 'iwilldoagreatjob',
            'password2': 'iwilldoagreatjob'}

    def test_register_shipper_invalid(self):
        """
        Test if the registration of an invalid shipper keeps the user in the shipper registration page.
        """

        response = self.client.post(
            reverse('users:register_shipper'), self.data_invalid, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_carrier_invalid(self):
        """
        Test if the registration of an invalid carrier keeps the user in the carrier registration page.
        """

        response = self.client.post(
            reverse('users:register_carrier'), self.data_invalid, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_shipper_redirect(self):
        """
        Test if the registration of an valid shipper redirects the user to the login page.
        """

        response = self.client.post(
            reverse('users:register_shipper'), self.data_shipper, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('users:login'))

    def test_register_carrier_redirect(self):
        """
        Test if the registration of an valid carrier redirects the user to the login page.
        """

        response = self.client.post(
            reverse('users:register_carrier'), self.data_carrier, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('users:login'))
