from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from load.models import Load
from users.models import Carrier
from load.api.serializers import CarrierLoadSerializer, ShipperLoadSerializer, CreateLoadSerializer
from load import utils
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
            return Load.objects.filter(shipper=self.request.user)

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
        queryset = Load.objects.filter(
            carrier=None, shipper_id=request.user.pk)
        serializer = ShipperLoadSerializer(queryset, many=True)

        return Response(serializer.data)

    def carrier_available(self, request):
        carrier = Carrier.objects.get(user=request.user.pk)
        rejected_loads = carrier.dropped_by.all()
        queryset = Load.objects.filter(
            carrier=None).exclude(id__in=rejected_loads)
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
        queryset = Load.objects.exclude(
            carrier=None).filter(shipper=request.user)
        serializer = ShipperLoadSerializer(queryset, many=True)

        return Response(serializer.data)

    def carrier_accepted(self, request):
        carrier = Carrier.objects.get(user=request.user.pk)
        queryset = Load.objects.filter(carrier=carrier)
        serializer = CarrierLoadSerializer(queryset, many=True)

        return Response(serializer.data)

    # Rejected loads list
    @action(methods=['get'], detail=False)
    def rejected(self, request):
        self.serializer_class = self.get_serializer_class()
        carrier = Carrier.objects.get(user=request.user.pk)
        loads = carrier.dropped_by.all()
        serializer = CarrierLoadSerializer(loads, many=True)

        return Response(serializer.data)

    # Accept load
    @action(methods=['post'], detail=True)
    def accept(self, request, pk=None):
        self.serializer_class = self.get_serializer_class()
        carrier = Carrier.objects.get(user=request.user.pk)
        load = get_object_or_404(Load, pk=pk, carrier=None)
        serializer = CarrierLoadSerializer(
            load, data={'carrier': carrier.pk}, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Reject load
    @action(methods=['post'], detail=True)
    def reject(self, request, pk=None):
        self.serializer_class = self.get_serializer_class()
        carrier = Carrier.objects.get(user=request.user.pk)
        load_ = get_object_or_404(Load, pk=pk, carrier=None)

        if not carrier in load_.dropped_by.all():
            load_.dropped_by.add(carrier)

            return Response(status.HTTP_201_CREATED)

        return Response(data={'detail': "Load already dropped"})
