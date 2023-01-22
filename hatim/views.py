from rest_framework.views import Response
from rest_framework import generics, status
from rest_framework.permissions import *
from .models import *
from .serializers import *
from .permissions import *
from user_auth.models import CustomUser as User


class HatimViewSet(generics.ListAPIView):
    queryset = Hatim.objects.all()
    serializer_class = HatimSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Hatim.objects.filter(isCompleted=False)


class HatimRetrieveView(generics.RetrieveAPIView):
    queryset = Hatim.objects.all()
    serializer_class = SingleHatimSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get(self, request, pk, format=None):
        queryset = Hatim.objects.get(pk=pk)
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
            if isAllCompleted(juz.hatim_id):
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
                hatim = Hatim.objects.get(pk=juz.hatim_id.id)
                hatim.isCompleted = True
                hatim.save()

                if hatim.isPublic == True:
                    #create new public hatim when one of them completed
                    create_public_hatim(hatim.creator_id)
                else:
                    user = User.objects.get(pk=hatim.creator_id.id)
                    user.active_hatims -= 1
                    user.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {'message':'You are not the owner of this juz'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


def create_public_hatim(user):
    hatim_deadine = datetime.date.today() + datetime.timedelta(days=30)
    hatim = Hatim.objects.create(creator_id=user, isCompleted=False, isPublic=True, title='hatim.io', description='ARO', deadline=hatim_deadine)
    hatim.save()


def isAllCompleted(hatim_id):
    juzs = Juz.objects.filter(hatim_id=hatim_id, type='juz')
    for juz in juzs:
        if juz.status != 'completed':
            return False
    return True