from rest_framework.serializers import ModelSerializer
from load.models import Load
from users.models import Shipper


class ShipperSerializer(ModelSerializer):
    class Meta:
        model = Shipper
        fields = ('first_name', 'last_name', 'email')


class ShipperLoadSerializer(ModelSerializer):
    shipper = ShipperSerializer()

    class Meta:
        model = Load
        fields = ('shipper', 'carrier', 'pickup_date', 'ref',
                  'origin_city', 'destination_city', 'shipper_price')


class CarrierLoadSerializer(ModelSerializer):
    shipper = ShipperSerializer()

    class Meta:
        model = Load
        fields = ('shipper', 'carrier', 'pickup_date', 'ref',
                  'origin_city', 'destination_city', 'carrier_price')


class CreateLoadSerializer(ModelSerializer):
    class Meta:
        model = Load
        fields = ('pickup_date', 'ref', 'origin_city', 'destination_city', 'shipper_price')
