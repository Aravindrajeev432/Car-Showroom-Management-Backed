from django.urls import path

from .views import AddParts, PartUpdator, UniCarPartNumbers

urlpatterns = [
    path("parts", AddParts.as_view()),
    path("unicarpartnumbers", UniCarPartNumbers.as_view()),
    path("update-part/<int:pk>", PartUpdator.as_view()),
]
