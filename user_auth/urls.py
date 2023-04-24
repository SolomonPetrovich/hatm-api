from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("users/me/", UserRetrieveUpdateDestroyAPIView.as_view()),
]
