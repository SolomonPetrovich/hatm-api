from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("users/me/", UserRetriveUpdateView.as_view()),
    path('login/google/', GoogleSocialAuthView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())
]
