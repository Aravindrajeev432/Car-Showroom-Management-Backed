from django.urls import path

from .views import GetMyCars, ServiceHistoryUser, TestingChannel, UserLogin

urlpatterns = [
    path("usertest", UserLogin.as_view(), name="index"),
    path("mycars", GetMyCars.as_view(), name="mycars"),
    path("userchannel", TestingChannel.as_view()),
    path("servicehistory/<int:pk>", ServiceHistoryUser.as_view()),
]
