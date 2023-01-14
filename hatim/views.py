from django.shortcuts import render
from rest_framework.views import Response
from rest_framework import generics, status
from rest_framework.permissions import *
from .models import *
from .serializers import *
from .permissions import *


class HatimViewSet(generics.ListAPIView):
    queryset = Hatim.objects.all()
    serializer_class = HatimSerializer
    permission_classes = (IsAuthenticated, )


class HatimCreateAPIView(generics.CreateAPIView):
    queryset = Hatim.objects.all()
    serializer_class = SingleHatimSerializer
    permission_classes = (HatimCountPermission, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class HatimRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Hatim.objects.all()
    serializer_class = SingleHatimSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get(self, request, pk, format=None):
        queryset = Hatim.objects.get(pk=pk)
        serializer = self.serializer_class(queryset, context={'request':self.get_serializer_context()})
        return Response(serializer.data)


class JuzViewSet(generics.ListAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )


class JuzAPIView(generics.RetrieveAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )


class JuzTakeAPIView(generics.GenericAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )
    
    def patch(self, request, pk, format=None):
        juz = self.get_object()
        juz.status = "in Progress"
        juz.user_id = request.user
        juz.save()
        serializer = self.get_serializer(juz)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JuzCancelAPIView(generics.GenericAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer
    permission_classes = (IsOwnerOnly, )

    def patch(self, request, pk, format=None):
        juz = self.get_object()
        juz.status = "free"
        juz.user_id = None
        juz.save()
        serializer = self.get_serializer(juz)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JuzFinishAPIView(generics.GenericAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer
    permission_classes = (IsOwnerOnly, )

    def patch(self, request, pk, format=None):
        juz = self.get_object()
        juz.status = "completed"
        juz.save()
        serializer = self.get_serializer(juz)
        return Response(serializer.data, status=status.HTTP_200_OK)
