from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class EmailUserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
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
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
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
    def get_shipper(self, request):
        return self.get(user=request.user.pk)


class Shipper(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    objects = ShipperManager()


class CarrierManager(models.Manager):
    def get_carrier(self, request):
        return self.get(user=request.user.pk)


class Carrier(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    mc_number = models.CharField(max_length=12)

    objects = CarrierManager()
