import asyncio
import time

from channels.layers import get_channel_layer
from django.contrib.auth import authenticate
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from cars.models import Cars
from services.models import ServiceHistory

from .serializers import MyCarsSerializer, ServiceHistorySerializer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["phone_number"] = user.phone_number

        # ...

        return token


class UserLogin(APIView, TokenObtainPairSerializer):

    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["phone_number"] = user.phone_number

        # ...
        print(token.access_token)
        return token

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return self.get_token(refresh)
        # return {
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token),
        # }

    def post(self, request):

        data = request.data
        user = authenticate(username=data["username"], password=data["password"])

        if user is None:

            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # checking for staff members is customer or not
        elif not user.is_customer:

            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.is_customer:
            # token = self.get_tokens_for_user(user)
            token = self.get_token(user)
            data = {"refresh": str(token), "access": str(token.access_token)}

        return Response(data=data, status=status.HTTP_200_OK)


class GetMyCars(AutoPrefetchViewSetMixin, generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    model = Cars
    serializer_class = MyCarsSerializer

    def get_queryset(self):
        # user= Account.objects.get(id=self.request.user)
        return Cars.objects.filter(user=self.request.user).order_by("id")


# class GetMyCars(APIView):
#     def get(self,request):
#         permission_classes = [IsAuthenticated]
#         query = Cars.objects.filter(user=self.request.user)
#         serializer_classobj = MyCarsSerializer(query,many=True,context={'id':'sad'})
#
#         return Response(serializer_classobj.data)
#         def get_queryset(self):
#             # user= Account.objects.get(id=self.request.user)
#             return Cars.objects.filter(user=self.request.user)


class TestingChannel(APIView):
    def get(self, request):
        channel_layer = get_channel_layer()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            channel_layer.group_send(
                "notification_12", {"type": "notificator", "message": "my message"}
            )
        )

        # async_to_sync(channel_layer.group_send)(
        #     'notification_12',
        #     {
        #         'type':'notificator',
        #         'message':'my message'
        #     }
        # )
        return Response(status=status.HTTP_200_OK)


class ServiceHistoryUser(APIView):
    def get(self, request, pk):
        print(pk)
        time.sleep(2)
        ser = ServiceHistory.objects.filter(service__car=pk)
        serializerObj = ServiceHistorySerializer(ser, many=True)
        return Response(serializerObj.data, status=status.HTTP_200_OK)
