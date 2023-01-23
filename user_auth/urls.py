from django.urls import path
from .views import *


urlpatterns = [
    path("me/", UserRetrieveAPIView.as_view(), name=""),
]
