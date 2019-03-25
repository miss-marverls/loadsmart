from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Load(models.Model):
    shipper = models.ForeignKey(
        User, related_name='shipper', on_delete=models.CASCADE)
    carrier = models.ForeignKey(
        User, related_name='carrier', on_delete=models.CASCADE, null=True, blank=True)
    pickup_date = models.DateTimeField()
    ref = models.CharField(max_length=200)
    origin_city = models.CharField(max_length=200)
    destination_city = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return self.ref