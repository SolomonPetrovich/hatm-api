from django.urls import path
from .views import *


urlpatterns = [
    path("users/me/", UserRetriveUpdateView.as_view()),
    path('login/google/', GoogleSocialAuthView.as_view()),
]
