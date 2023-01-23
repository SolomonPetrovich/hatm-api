from rest_framework import generics, response, status, permissions
from .serializers import *
from .models import CustomUser as User
from .permissions import *


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOnly, )
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user