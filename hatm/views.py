from rest_framework.views import Response
from rest_framework import generics, status
from rest_framework.permissions import *
from .models import *
from .serializers import *
from .permissions import *
from user_auth.models import CustomUser as User


class HatmViewSet(generics.ListAPIView):
    queryset = Hatm.objects.all()
    serializer_class = HatmSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Hatm.objects.filter(isCompleted=False)


class HatmRetrieveView(generics.RetrieveAPIView):
    queryset = Hatm.objects.all()
    serializer_class = SingleHatmSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get(self, request, pk, format=None):
        queryset = Hatm.objects.get(pk=pk)
        serializer = self.serializer_class(queryset, context={'request':self.get_serializer_context()})
        return Response(serializer.data)


class JuzMineViewSet(generics.ListAPIView):
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Juz.objects.filter(user_id=user)


class JuzTakeView(generics.GenericAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )
    
    def patch(self, request, pk, format=None):
        juz = self.get_object()
        if juz.type == 'dua':
            if isAllCompleted(juz.hatm_id):
                juz.status = 'in Progress'
                juz.user_id = request.user
                juz.save()
                serializer = self.get_serializer(juz)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = {'message':'All Juz are not completed'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if juz.status == 'free':
            juz.status = 'in Progress'
            juz.user_id = request.user
            juz.save()
            serializer = self.get_serializer(juz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {'message':'Juz is already taken or finished'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class JuzCancelView(generics.GenericAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )

    def patch(self, request, pk, format=None):
        juz = self.get_object()
        if juz.user_id == request.user:
            juz.status = 'free'
            juz.user_id = None
            juz.save()
            serializer = self.get_serializer(juz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {'message':'You are not the owner of this juz'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class JuzFinishView(generics.GenericAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )

    def patch(self, request, pk, format=None):
        juz = self.get_object()
        if juz.user_id == request.user:
            juz.status = 'completed'
            juz.save()
            serializer = self.get_serializer(juz)

            if juz.type == 'dua':
                hatm = Hatm.objects.get(pk=juz.hatm_id.id)
                hatm.isCompleted = True
                hatm.save()

                if hatm.isPublic == True:
                    #create new public hatm when one of them completed
                    create_public_hatm(hatm.creator_id)
                else:
                    user = User.objects.get(pk=hatm.creator_id.id)
                    user.active_hatms -= 1
                    user.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {'message':'You are not the owner of this juz'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


def create_public_hatm(user):
    hatm_deadine = datetime.date.today() + datetime.timedelta(days=30)
    hatm = Hatm.objects.create(creator_id=user, isCompleted=False, isPublic=True, title='hatm.io', description='ARO', deadline=hatm_deadine)
    hatm.save()


def isAllCompleted(hatm_id):
    juzs = Juz.objects.filter(hatm_id=hatm_id, type='juz')
    for juz in juzs:
        if juz.status != 'completed':
            return False
    return True