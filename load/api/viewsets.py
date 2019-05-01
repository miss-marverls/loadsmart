from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from load import utils
from load.api.serializers import CarrierLoadSerializer, ShipperLoadSerializer, CreateLoadSerializer
from load.models import Load
from users.models import Shipper, Carrier
from .permissions import CanAccess


class LoadViewSet(ModelViewSet):
    serializer_class = ''
    permission_classes = (IsAuthenticated, CanAccess,)
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.request.user.is_shipper:
            if self.action == 'create':
                return CreateLoadSerializer

            return ShipperLoadSerializer

        return CarrierLoadSerializer

    def get_queryset(self):
        self.serializer_class = self.get_serializer_class()

        if self.request.user.is_shipper:
            shipper = Shipper.objects.get(user=self.request.user.pk)
            return Load.objects.filter(shipper=shipper)

        return Load.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CreateLoadSerializer(data=request.data)
        carrier_price = utils.calculate_carrier_price(request.data["shipper_price"])
        if serializer.is_valid():
            serializer.save(shipper_id=request.user.pk,
                            carrier_price=carrier_price)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Available loads list
    @action(methods=['get'], detail=False)
    def available(self, request):
        self.serializer_class = self.get_serializer_class()
        if self.request.user.is_shipper:
            return self.shipper_available(request)

        return self.carrier_available(request)

    def shipper_available(self, request):
        queryset = Load.objects.get_shipper_available_loads(request)
        serializer = ShipperLoadSerializer(queryset, many=True)

        return Response(serializer.data)

    def carrier_available(self, request):
        queryset = Load.objects.get_carrier_available_loads(request)
        serializer = CarrierLoadSerializer(queryset, many=True)

        return Response(serializer.data)

    # Accepted loads list
    @action(methods=['get'], detail=False)
    def accepted(self, request):
        self.serializer_class = self.get_serializer_class()

        if self.request.user.is_shipper:
            return self.shipper_accepted(request)

        return self.carrier_accepted(request)

    def shipper_accepted(self, request):
        queryset = Load.objects.get_shipper_accepted_loads(request)
        serializer = ShipperLoadSerializer(queryset, many=True)

        return Response(serializer.data)

    def carrier_accepted(self, request):
        queryset = Load.objects.get_carrier_accepted_loads(request)
        serializer = CarrierLoadSerializer(queryset, many=True)

        return Response(serializer.data)

    # Rejected loads list
    @action(methods=['get'], detail=False)
    def rejected(self, request):
        self.serializer_class = self.get_serializer_class()
        queryset = Load.objects.get_carrier_rejected_loads(request)
        serializer = CarrierLoadSerializer(queryset, many=True)

        return Response(serializer.data)

    # Accept load
    @action(methods=['post'], detail=True)
    def accept(self, request, pk=None):
        self.serializer_class = self.get_serializer_class()
        carrier = Carrier.objects.get_carrier(request)
        load = get_object_or_404(Load, pk=pk, carrier=None)
        serializer = CarrierLoadSerializer(
            load, data={'carrier': carrier.pk}, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_201_CREATED, data=serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Reject load
    @action(methods=['post'], detail=True)
    def reject(self, request, pk=None):
        self.serializer_class = self.get_serializer_class()
        carrier = Carrier.objects.get(user=request.user.pk)
        load_ = get_object_or_404(Load, pk=pk, carrier=None)

        if not carrier in load_.dropped_by.all():
            load_.dropped_by.add(carrier)

            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': "Load already dropped"})
