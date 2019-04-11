from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from load.models import Load, DroppedLoads
from load.api.serializers import LoadSerializer, DroppedLoadSerializer


class LoadViewSet(ModelViewSet):
    serializer_class = LoadSerializer

    def get_queryset(self):
        return Load.objects.filter(shipper=self.request.user)

    @action(methods=['get'], detail=False)
    def available(self, request):
        queryset = Load.objects.filter(carrier=None, shipper=request.user)
        serializer = LoadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def accepted(self, request):
        queryset1 = Load.objects.exclude(carrier=None)
        queryset2 = Load.objects.filter(shipper=request.user)
        serializer = LoadSerializer(queryset1 & queryset2, many=True)
        return Response(serializer.data)


class CarrierLoadViewSet(ModelViewSet):
    serializer_class = LoadSerializer

    def get_queryset(self):
        return Load.objects.all()

    @action(methods=['get'], detail=False)
    def accepted(self, request):
        queryset = Load.objects.filter(carrier=request.user.id)
        serializer = LoadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def available(self, request):
        queryset = Load.objects.filter(carrier=None)
        serializer = LoadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def accept(self, request, pk=None):
        load = get_object_or_404(Load, pk=pk, carrier=None)
        serializer = LoadSerializer(load, data={'carrier': request.user.id}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True)
    def drop(self, request, pk=None):
        load_ = get_object_or_404(Load, pk=pk, carrier=None)
        dropped_ = DroppedLoads.objects.filter(load=load_)
        if len(dropped_) == 0:
            dropped_load = DroppedLoads(load=load_, carrier=request.user)
            dropped_load.save()
            serializer = DroppedLoadSerializer(dropped_load)
            return Response(serializer.data)
        return Response(data={'detail': "Load already dropped"})

