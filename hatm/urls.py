from django.urls import path
from .views import *

urlpatterns = [
    #hatm
    path('hatm/', HatmViewSet.as_view()),
    path('hatm/<uuid:pk>/', HatmRetrieveView.as_view()),
    path('hatm/<uuid:pk>/juzs/', JuzViewSet.as_view()),
    path('hatm/mine/', HatmMineViewSet.as_view()),
    path("hatm/created/", HatmCreatedViewSet.as_view()),

    #juzs
    path('juzs/mine/', JuzMineViewSet.as_view()),
    path('juzs/take/', JuzTakeView.as_view()),
    path('juzs/cancel/<uuid:pk>/', JuzCancelView.as_view()),
    path('juzs/finish/<uuid:pk>/', JuzFinishView.as_view()),
]