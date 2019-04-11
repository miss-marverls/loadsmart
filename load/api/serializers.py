from rest_framework.serializers import ModelSerializer
from load.models import Load, DroppedLoads


class LoadSerializer(ModelSerializer):
    class Meta:
        model = Load
        fields = ('shipper', 'carrier', 'pickup_date', 'ref',
                  'origin_city', 'destination_city', 'price')


class DroppedLoadSerializer(ModelSerializer):
    class Meta:
        model = DroppedLoads
        fields = ('load', 'carrier')
