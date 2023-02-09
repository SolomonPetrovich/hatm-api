from rest_framework import generics, status
from rest_framework.permissions import *
from .serializers import *
from .models import CustomUser as User
from .permissions import *
from rest_framework.response import Response


class UserRetriveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user