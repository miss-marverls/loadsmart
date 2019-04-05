from rest_framework.serializers import ModelSerializer
from load.models import Load


class LoadSerializer(ModelSerializer):
    class Meta:
        model = Load
        fields = ('shipper', 'carrier', 'pickup_date', 'ref',
                  'origin_city', 'destination_city', 'price')
