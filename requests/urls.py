from django.urls import path

from .views import CarEnquiryListCreate, CarEnquiryupdate, Enquiry

urlpatterns = [
    path("get_enquires", CarEnquiryListCreate.as_view(), name="get_enquires"),
    path("enquiry", Enquiry.as_view(), name="enquiry"),
    path("enquiry/<int:pk>", CarEnquiryupdate.as_view()),
]
