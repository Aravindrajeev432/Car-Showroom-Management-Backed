from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework import filters, generics

from cars.models import CarParts, UniPartNumbers

from .pagination import PartsPagination
from .serializers import (
    CarPartsSerializer,
    CarPartUpdateSerializer,
    UniCarPartsSerializer,
)


# Create your views here.
class AddParts(AutoPrefetchViewSetMixin, generics.ListCreateAPIView):
    serializer_class = CarPartsSerializer
    queryset = CarParts.objects.all()
    pagination_class = PartsPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["unique_part_name"]


class UniCarPartNumbers(generics.ListAPIView):
    serializer_class = UniCarPartsSerializer
    queryset = UniPartNumbers.objects.all()


class PartUpdator(AutoPrefetchViewSetMixin, generics.RetrieveUpdateAPIView):
    serializer_class = CarPartUpdateSerializer
    queryset = CarParts.objects.all()
    lookup_field = "pk"
