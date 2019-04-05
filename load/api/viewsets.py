from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from load.models import Load
from load.api.serializers import LoadSerializer


class LoadViewSet(ModelViewSet):
    queryset = Load.objects.filter()
    serializer_class = LoadSerializer

    @action(methods=['get'], detail=False)
    def available(self, request):
        queryset = Load.objects.filter(carrier=None)
        serializer = LoadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def accepted(self, request):
        queryset = Load.objects.exclude(carrier=None)
        serializer = LoadSerializer(queryset, many=True)
        return Response(serializer.data)
