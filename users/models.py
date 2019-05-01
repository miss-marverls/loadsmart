from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class EmailUserManager(BaseUserManager):
    """A manager for user creation with email and password."""

    def create_user(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        :rtype:
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

        :param args:
        :param kwargs:
        :return:
        :rtype:
        """

        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    """Stores user information.

    User fields are: email, first_name, last_name, is_shipper, is_carrier. The email is set to be the username.
    The boolean fields is_shipper and is_carrier define the type of user. Inherits EmailUserManager methods.
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
    """A manager to access shipper information."""

    def get_shipper(self, request):
        """Gets the User primary key.

        :param HttpRequest request: HttpRequest object
        :return: The Shipper that matches the primary key
        :rtype: Shipper
        """

        return self.get(user=request.user.pk)


class Shipper(models.Model):
    """Stores the information about Shippers.

    Shipper field is a foreign key from a User. Inherits ShipperManager methods.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    objects = ShipperManager()


class CarrierManager(models.Manager):
    """A manager to access Carrier information."""

    def get_carrier(self, request):
        """Gets the User primary key.

        :param HttpRequest request: HttpRequest object
        :return: The Carrier that matches the primary key
        :rtype: Carrier
        """

        return self.get(user=request.user.pk)


class Carrier(models.Model):
    """Stores the information about Carries.

    Carrier fields are a foreign key from a User and the mc_number. Inherits CarrierManager methods.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    mc_number = models.CharField(max_length=12)

    objects = CarrierManager()
