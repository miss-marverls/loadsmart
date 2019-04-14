from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from load.models import Load
from load.api.serializers import LoadSerializer, CreateLoadSerializer


class LoadViewSet(ModelViewSet):
    serializer_class = LoadSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateLoadSerializer
        return LoadSerializer

    def get_queryset(self):
        return Load.objects.filter(shipper=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CreateLoadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(shipper_id=request.user.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def available(self, request):
        queryset = Load.objects.filter(carrier=None, shipper_id=request.user.pk)
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
        dropped_loads = request.user.dropped_by.all()
        queryset = Load.objects.filter(carrier=None).exclude(id__in=dropped_loads)
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
        if not request.user in load_.dropped_by.all():
            load_.dropped_by.add(request.user)
            return Response(status.HTTP_201_CREATED)
        return Response(data={'detail': "Load already dropped"})

    @action(methods=['get'], detail=False)
    def dropped(self, request):
        loads = request.user.dropped_by.all()
        serializer = LoadSerializer(loads, many=True)
        return Response(serializer.data)

