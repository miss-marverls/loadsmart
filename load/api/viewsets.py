from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from load.models import Load
from users.models import Carrier
from load.api.serializers import CarrierLoadSerializer, ShipperLoadSerializer, CreateLoadSerializer


class LoadViewSet(ModelViewSet):
    serializer_class = ShipperLoadSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateLoadSerializer
        return ShipperLoadSerializer

    def get_queryset(self):
        return Load.objects.filter(shipper=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CreateLoadSerializer(data=request.data)
        carrier_price_ = request.data["shipper_price"] - request.data["shipper_price"] * 5 / 100
        if serializer.is_valid():
            serializer.save(shipper_id=request.user.pk, carrier_price=carrier_price_)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def available(self, request):
        queryset = Load.objects.filter(carrier=None, shipper_id=request.user.pk)
        serializer = ShipperLoadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def accepted(self, request):
        queryset1 = Load.objects.exclude(carrier=None)
        queryset2 = Load.objects.filter(shipper=request.user)
        serializer = ShipperLoadSerializer(queryset1 & queryset2, many=True)
        return Response(serializer.data)


class CarrierLoadViewSet(ModelViewSet):
    serializer_class = CarrierLoadSerializer

    def get_queryset(self):
        return Load.objects.all()

    @action(methods=['get'], detail=False)
    def accepted(self, request):
        carrier = Carrier.objects.get(user=request.user.pk)
        queryset = Load.objects.filter(carrier=carrier)
        serializer = CarrierLoadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def available(self, request):
        carrier = Carrier.objects.get(user=request.user.pk)
        dropped_loads = carrier.dropped_by.all()
        queryset = Load.objects.filter(carrier=None).exclude(id__in=dropped_loads)
        serializer = CarrierLoadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def accept(self, request, pk=None):
        carrier = Carrier.objects.get(user=request.user.pk)
        load = get_object_or_404(Load, pk=pk, carrier=None)
        serializer = CarrierLoadSerializer(load, data={'carrier': carrier.pk}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True)
    def drop(self, request, pk=None):
        carrier = Carrier.objects.get(user=request.user.pk)
        load_ = get_object_or_404(Load, pk=pk, carrier=None)
        if not carrier in load_.dropped_by.all():
            load_.dropped_by.add(carrier)
            return Response(status.HTTP_201_CREATED)
        return Response(data={'detail': "Load already dropped"})

    @action(methods=['get'], detail=False)
    def dropped(self, request):
        carrier = Carrier.objects.get(user=request.user.pk)
        loads = carrier.dropped_by.all()
        serializer = CarrierLoadSerializer(loads, many=True)
        return Response(serializer.data)
