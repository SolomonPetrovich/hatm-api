from rest_framework import generics, response, status, permissions
from .serializers import *
from .models import CustomUser as User
from .permissions import *

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return response.Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            },
            status=status.HTTP_201_CREATED,
        )


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOnly, )
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user