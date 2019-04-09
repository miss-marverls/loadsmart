from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from load.models import Load
from load.api.serializers import LoadSerializer


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
