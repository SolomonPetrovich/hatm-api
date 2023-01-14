from django.urls import path
from .views import *

urlpatterns = [
    path('hatim/', HatimViewSet.as_view()),
    path('hatim/<int:pk>/', HatimRetrieveDestroyView.as_view()),
    path("hatim/create/", HatimCreateAPIView.as_view()),
    path('juz/', JuzViewSet.as_view()),
    path('juz/<int:pk>/', JuzAPIView.as_view()),
    path("juz/take/<int:pk>/", JuzTakeAPIView.as_view()),
    path('juz/cancel/<int:pk>/', JuzCancelAPIView.as_view()),
    path("juz/finish/<int:pk>/", JuzFinishAPIView.as_view())
]