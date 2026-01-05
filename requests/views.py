# Create your views here.
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from frontdesk.models import CarEnquiresmodel

from .pagination import EnquiryPagination
from .serializers import (
    CarEnquiresSerializer,
    CarEnquiryListCreateSerializer,
    EnquireySerilaizer,
)


class Enquiry(APIView):
    def post(self, request):

        serializerobj = CarEnquiresSerializer(data=request.data)
        if serializerobj.is_valid():
            serializerobj.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "enqgroup",
                {
                    "type": "enq_message",
                    "message": serializerobj.data,
                },
            )

            return Response(data=serializerobj.data, status=status.HTTP_201_CREATED)
        else:
            print(serializerobj.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetEnquires(APIView):

    def get(self, request):
        enqs = CarEnquiresmodel.objects.select_related("user").all()
        serializerobj = CarEnquiresSerializer(enqs, many=True)

        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     'enqgroup',
        #     {
        #         'type': 'enq_message',
        #         'message': serializerobj.data,
        #     }
        # )

        return Response(data=serializerobj.data, status=status.HTTP_200_OK)


class CarEnquiryListCreate(generics.ListCreateAPIView):
    pagination_class = EnquiryPagination
    serializer_class = CarEnquiryListCreateSerializer
    queryset = CarEnquiresmodel.objects.all().order_by("-created_at")


class CarEnquiryupdate(generics.UpdateAPIView):
    lookup_field = "pk"
    serializer_class = EnquireySerilaizer
    queryset = CarEnquiresmodel.objects.all()
