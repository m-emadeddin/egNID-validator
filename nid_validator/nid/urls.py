from django.urls import path

from .views import NationalIdValidatorAPIView

urlpatterns = [
    path("id/<str:id>/", NationalIdValidatorAPIView.as_view(), name="nid-validator"),
]
