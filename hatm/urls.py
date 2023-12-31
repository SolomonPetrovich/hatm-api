from django.urls import path
from .views import *

urlpatterns = [
    path('hatm/', HatmViewSet.as_view()),
    path('hatm/<int:pk>/', HatmRetrieveView.as_view()),
    path('hatm/<int:pk>/juzs/', JuzViewSet.as_view()),
    path('hatm/mine/', HatmMineViewSet.as_view()),
    path('juzs/mine/', JuzMineViewSet.as_view()),
    path('juzs/take/', JuzTakeView.as_view()),
    path('juzs/cancel/<int:pk>/', JuzCancelView.as_view()),
    path('juzs/finish/<int:pk>/', JuzFinishView.as_view()),
]