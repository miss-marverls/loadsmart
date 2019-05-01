from rest_framework.serializers import ModelSerializer

from load.models import Load
from users.models import Shipper, Carrier, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ShipperSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Shipper
        fields = ('user',)


class CarrierSerializer(ModelSerializer):
    class Meta:
        model = Carrier
        fields = ('mc_number',)


class ShipperLoadSerializer(ModelSerializer):
    carrier = CarrierSerializer()

    class Meta:
        model = Load
        fields = ('shipper', 'carrier', 'pickup_date', 'ref',
                  'origin_city', 'destination_city', 'shipper_price')


class CarrierLoadSerializer(ModelSerializer):
    shipper = ShipperSerializer()

    class Meta:
        model = Load
        fields = ('id', 'shipper', 'carrier', 'pickup_date', 'ref',
                  'origin_city', 'destination_city', 'carrier_price')


class CreateLoadSerializer(ModelSerializer):
    class Meta:
        model = Load
        fields = ('pickup_date', 'ref', 'origin_city', 'destination_city', 'shipper_price')
