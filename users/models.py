from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext as _


class EmailUserManager(BaseUserManager):
    """
    A manager for User creation that requires an email and a password.
    """

    def create_user(self, *args, **kwargs):
        """
        Creates a User.

        :param args: Variable length argument list. Not used.
        :param kwargs: Key words sent to create_user method.
        :return: Created User
        :rtype: User
        """

        email = kwargs["email"]
        email = self.normalize_email(email)
        password = kwargs["password"]
        kwargs.pop("password")

        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        """
        Creates a User with super user privileges.

        :param args: Variable length argument list. Not used.
        :param kwargs: Key words sent to create_user method.
        :return: Created User
        :rtype: User
        """

        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    """
    Model for User.

    Stores User information in the fields: email, first_name, last_name, is_shipper, is_carrier.
    The email is set to be the username. The boolean fields is_shipper and is_carrier define
    the type of user. Uses EmailUserManager.
    """

    email = models.EmailField(
        verbose_name=_('Email address'),
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=50,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=50,
        blank=False,
    )
    is_shipper = models.BooleanField(default=False)
    is_carrier = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = EmailUserManager()


class ShipperManager(models.Manager):
    """
    A manager to access shipper information.
    """

    def get_shipper(self, request):
        """Gets the Shipper by the User primary key.

        :param django.http.HttpRequest request: Received request.
        :return: The Shipper that matches the User primary key.
        :rtype: Shipper
        """

        return self.get(user=request.user.pk)


class Shipper(models.Model):
    """
    Model for the Shipper

    Stores the information about Shippers. Shipper field is a foreign key from a User. Uses ShipperManager.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    objects = ShipperManager()


class CarrierManager(models.Manager):
    """
    A manager to access Carrier information.
    """

    def get_carrier(self, request):
        """Gets the Carrier by the User primary key.

        :param django.http.HttpRequest request: Received request.
        :return: The Carrier that matches the User primary key.
        :rtype: Carrier
        """

        return self.get(user=request.user.pk)


class Carrier(models.Model):
    """
    Stores the information about Carrie.

    Carrier fields are a foreign key from a User and the mc_number. Uses CarrierManager.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    mc_number = models.CharField(max_length=8)

    objects = CarrierManager()
