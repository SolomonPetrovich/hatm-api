from django.urls import path
from .views import *

urlpatterns = [
    path('hatim/', HatimViewSet.as_view()),
    path('hatim/<int:pk>/', HatimRetrieveView.as_view()),
    path("juzs/mine/", JuzMineViewSet.as_view()),
    path("juzs/take/<int:pk>", JuzTakeView.as_view()),
    path('juzs/cancel/<int:pk>', JuzCancelView.as_view()),
    path("juzs/finish/<int:pk>", JuzFinishView.as_view()),
]