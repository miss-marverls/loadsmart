from django.db import models
from django.contrib.auth.models import User
from users.models import Shipper, Carrier
from django.utils import timezone


# Create your models here.


class Load(models.Model):
    shipper = models.ForeignKey(
        Shipper, related_name='shipper', on_delete=models.PROTECT)
    carrier = models.ForeignKey(
        Carrier, related_name='carrier', on_delete=models.PROTECT, null=True, blank=True)
    pickup_date = models.DateField()
    ref = models.CharField(max_length=200)
    origin_city = models.CharField(max_length=200)
    destination_city = models.CharField(max_length=200)
    price = models.FloatField()
    dropped_by = models.ManyToManyField(Carrier, related_name="dropped_by")

    def __str__(self):
        return self.ref
