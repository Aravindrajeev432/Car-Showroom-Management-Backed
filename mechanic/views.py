from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.custom_permissions import IsMechanic
from cars.models import CarParts
from services.models import BayDetails, Services

from .serializers import (
    BayJoinSerializer,
    CompatiblePartsSerializer,
    CurrentJobFinisherSerializer,
    LiveBaySerializer,
    MakeBayFreeSerializer,
    MyCurrentJobSerializer,
    ServicePartsUpdatorSerializer,
)

# Create your views here.


class GetBays(AutoPrefetchViewSetMixin, generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LiveBaySerializer
    queryset = BayDetails.objects.all().order_by("id")

    def get_serializer_context(self):
        return {"request": self.request}


class BayJoin(generics.UpdateAPIView):
    serializer_class = BayJoinSerializer
    queryset = BayDetails.objects.all()
    lookup_field = "pk"


class MyCurrentJob(AutoPrefetchViewSetMixin, APIView):
    permission_classes = [IsMechanic]

    def get(self, request):
        bay_details = BayDetails.objects.get(mechanic_1=request.user)
        if bay_details.status == "busy":
            serializerobj = MyCurrentJobSerializer(bay_details)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(data=serializerobj.data, status=status.HTTP_200_OK)


class CompatibleParts(AutoPrefetchViewSetMixin, generics.ListAPIView):
    serializer_class = CompatiblePartsSerializer
    queryset = CarParts.objects.all()
    lookup_field = "id"


class ServicePartsUpdator(generics.UpdateAPIView):
    serializer_class = ServicePartsUpdatorSerializer
    queryset = Services.objects.all()
    lookup_field = "pk"


class ServiceMechanicCompleter(generics.UpdateAPIView):
    serializer_class = CurrentJobFinisherSerializer
    queryset = Services.objects.all()
    lookup_field = "pk"


class MakeBayFree(generics.UpdateAPIView):
    serializer_class = MakeBayFreeSerializer
    queryset = BayDetails.objects.all()
    lookup_field = "pk"
