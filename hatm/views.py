import random
from django.forms import ValidationError

from rest_framework import generics, status
from rest_framework.permissions import *
from rest_framework.views import Response

from .models import *
from .permissions import *
from .serializers import *


class HatmViewSet(generics.GenericAPIView):
    queryset = Hatm.objects.all()
    serializer_class = HatmSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def get(self, request, format=None):
        queryset = Hatm.objects.filter(is_completed=False, is_public=True, is_published=True)
        serializer = self.serializer_class(queryset, many=True, context={'request':self.get_serializer_context()})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request':self.get_serializer_context()})
        if serializer.is_valid():
            is_public = serializer.validated_data['is_public']
            serializer.save(creator_id=request.user, is_published=not is_public)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class HatmRetrieveView(generics.RetrieveAPIView):
    queryset = Hatm.objects.all()
    serializer_class = HatmSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get(self, request, pk, format=None):
        queryset = Hatm.objects.get(pk=pk)
        serializer = self.serializer_class(queryset, context={'request':self.get_serializer_context()})
        return Response(serializer.data, status=status.HTTP_200_OK)


class JuzViewSet(generics.ListAPIView):
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        hatm_id = self.kwargs['pk']
        return Juz.objects.filter(hatm_id=hatm_id, status='free')


class JuzMineViewSet(generics.ListAPIView):
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Juz.objects.filter(user_id=user)


class JuzTakeView(generics.GenericAPIView):
    serializer_class = JuzTakeSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Juz.objects.filter(pk__in=self.request.data['ids'])

    def patch(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            days = serializer.validated_data['days']
            queryset = self.get_queryset()
            taken_juzs = []
            succesfully = []
            for juz in queryset:
                if juz.status == 'free':
                    juz.status = 'in Progress'
                    juz.user_id = request.user
                    juz.deadline = datetime.datetime.now() + datetime.timedelta(days=days)
                    juz.save()
                    succesfully.append(juz.juz_number)
                else:
                    taken_juzs.append(juz.juz_number)
            
            if len(taken_juzs) > 0:
                data = {'already_taken':taken_juzs, 'succesfully_taken':succesfully}
                return Response(data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JuzCancelView(generics.GenericAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )

    def patch(self, request, pk, format=None):
        juz = self.get_object()
        if juz.user_id == request.user:
            juz.status = 'free'
            juz.user_id = None
            juz.deadline = None
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
        serializer = self.get_serializer(juz)

        if juz.user_id == request.user:
            
            if juz.type == 'dua':
                if is_all_completed(juz.hatm_id):
                    
                    juz.status = 'completed'
                    juz.save()
                    
                    hatm = Hatm.objects.get(pk=juz.hatm_id.id)
                    hatm.is_completed = True
                    hatm.save()
                    
                    overLimited = is_over_limited()
                    
                    if hatm.is_public == True:
                        if not overLimited:
                            create_public_hatm(hatm.creator_id)

                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    data = {'message':'All Juzs are not completed'}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                juz.status = 'completed'
                juz.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            data = {'message':'You are not the owner of this juz'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


def create_public_hatm(user):
    title_vars = [
        {
            'title': 'hatm.io',
            'description': 'ARO'
        },
        {
            'title': 'hatm.io',
            'description': 'ARO'
        },
        {
            'title': 'hatm.io',
            'description': 'ARO'
        }
    ]
    title_var = random.choice(title_vars)
    hatm_deadine = datetime.date.today() + datetime.timedelta(days=30)
    hatm = Hatm.objects.create(creator_id=user, is_completed=False, is_public=True, is_published=True, title=title_var['title'], description=title_var['description'], deadline=hatm_deadine)
    hatm.save()


def is_all_completed(hatm_id):
    juzs = Juz.objects.filter(hatm_id=hatm_id, type='juz')
    for juz in juzs:
        if juz.status != 'completed':
            return False
    return True


def is_over_limited():
    hatms = Hatm.objects.filter(is_public=True, is_published=True, is_completed=False)
    if len(hatms) >= 3:
        return True
    else:
        return False