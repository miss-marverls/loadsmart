from django.db import models
from django.contrib.auth.models import User
from users.models import Shipper, Carrier
from django.utils import timezone


# Create your models here.
class LoadManager(models.Manager):

    def get_carrier_available_loads(self, request):
        carrier = Carrier.objects.get_carrier(request)
        dropped_loads = carrier.dropped_by.all()

        return self.filter(
            carrier=None).exclude(id__in=dropped_loads)

    def get_carrier_accepted_loads(self, request):
        carrier = Carrier.objects.get_carrier(request)

        return self.filter(carrier=carrier)

    def get_carrier_rejected_loads(self, request):
        carrier = Carrier.objects.get_carrier(request)
        return carrier.dropped_by.all()

    def get_shipper_available_loads(self, request):
        shipper = Shipper.objects.get_shipper(request)

        return self.filter(carrier=None, shipper=shipper)

    def get_shipper_accepted_loads(self, request):
        shipper = Shipper.objects.get_shipper(request)

        return self.exclude(carrier=None).filter(shipper=shipper)


class Load(models.Model):
    shipper = models.ForeignKey(
        Shipper, related_name='shipper', on_delete=models.PROTECT)
    carrier = models.ForeignKey(
        Carrier, related_name='carrier', on_delete=models.PROTECT, null=True, blank=True)
    pickup_date = models.DateField()
    ref = models.CharField(max_length=200)
    origin_city = models.CharField(max_length=200)
    destination_city = models.CharField(max_length=200)
    shipper_price = models.FloatField()
    carrier_price = models.FloatField()
    dropped_by = models.ManyToManyField(Carrier, related_name="dropped_by")

    objects = LoadManager()

    def __str__(self):
        return self.ref
