from rest_framework import generics, status
from rest_framework.permissions import *
from rest_framework.views import Response

from .models import *
from .permissions import *
from .serializers import *

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .utils import *


class HatmViewSet(generics.GenericAPIView):
    queryset = Hatm.objects.all()
    serializer_class = HatmSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    @swagger_auto_schema(
        operation_description='Get all public, not completed, published hatms',
        responses={200: HatmSerializer(many=True)},
    )
    def get(self, request, format=None):
        queryset = Hatm.objects.filter(is_completed=False, is_public=True, is_published=True)
        serializer = self.serializer_class(queryset, many=True, context={'request':self.get_serializer_context()})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description='Create a new hatm',
        request_body=HatmSerializer,
        responses={201: HatmSerializer},
    )
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

    @swagger_auto_schema(
        operation_description='Get a specific hatm',
        responses={200: HatmSerializer},
    )
    def get(self, request, pk, format=None):
        queryset = Hatm.objects.get(pk=pk)
        serializer = self.serializer_class(queryset, context={'request':self.get_serializer_context()})
        return Response(serializer.data, status=status.HTTP_200_OK)


class HatmMineViewSet(generics.ListAPIView):
    '''Get list of hatm with specific juzs that taken by user'''
    serializer_class = HatmSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Hatm.objects.filter(juz__user_id=user)
    
    @swagger_auto_schema(
        operation_description='Get a list of hatm with juzs that are taken by the user',
        responses={200: HatmSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request':self.get_serializer_context()})
        data = serializer.data
        for hatm in data:
            juzs = hatm['juz']
            updated_juzs = []
            for juz in juzs:
                if 'user_id' in juz:
                    if juz['user_id'] == self.request.user.id:
                        updated_juzs.append(juz)
            hatm['juz'] = updated_juzs
        return Response(data, status=status.HTTP_200_OK)
    

class JuzViewSet(generics.ListAPIView):
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        hatm_id = self.kwargs['pk']
        return Juz.objects.filter(hatm_id=hatm_id, status='free')
    
    @swagger_auto_schema(
        operation_description='Get a list of free juz in a hatm',
        responses={200: JuzSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description='Hatm id', type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class JuzMineViewSet(generics.ListAPIView):
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Juz.objects.filter(user_id=user)
    
    @swagger_auto_schema(
        operation_description='Get a list of juz that are taken by the user',
        responses={200: JuzSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class JuzTakeView(generics.GenericAPIView):
    serializer_class = JuzTakeSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Juz.objects.filter(pk__in=self.request.data['ids'])

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'already_taken': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)),
                'succesfully_taken': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)),
                'deadline': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                }
            )
        },
        request_body=JuzTakeSerializer,
        operation_description='Take a list of juz for a number of days'
    )
    def patch(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            days = serializer.validated_data['days']
            queryset = self.get_queryset()
            taken_juzs = []
            succesfully = []
            unseccesfully = []
            for juz in queryset:
                if juz.type == 'juz':
                    if juz.status == 'free':
                        juz.status = 'in Progress'
                        juz.user_id = request.user
                        juz.deadline = datetime.datetime.now() + datetime.timedelta(days=days)
                        juz.save()
                        succesfully.append(juz.juz_number)
                    else:
                        taken_juzs.append(juz.juz_number)
                else:
                    unseccesfully.append(juz.juz_number)
                deadline = datetime.datetime.now() + datetime.timedelta(days=days)

            if len(succesfully) < 0:
                deadline = None
            data = {'already_taken': taken_juzs, 'succesfully_taken': succesfully, 'unsuccesfully_taken':unseccesfully, 'deadline': deadline.strftime(format='%Y-%m-%d %H:%M:%S')}
            return Response(data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JuzCancelView(generics.GenericAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
            responses={status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    },
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description='Juz id', type=openapi.TYPE_INTEGER), 
    ],
    operation_description='This view takes a list of juz ids and cancels them. It returns a list of juz numbers that were already cancelled and a list of juz numbers that were succesfully cancelled.',
    operation_id='juz_cancel',
    )
    def patch(self, request, pk, format=None):
        juz = self.get_object()
        if juz.user_id == request.user:
            juz.status = 'free'
            juz.user_id = None
            juz.deadline = None
            juz.save()
            data = {'message': 'Juz cancelled succesfully'}
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {'message':'You are not the owner of this juz'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class JuzFinishView(generics.GenericAPIView):
    queryset = Juz.objects.all()
    serializer_class = JuzSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
        },
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description='Juz id', type=openapi.TYPE_INTEGER),
        ],
        operation_description='This view takes a list of juz ids and finishes them. It returns a list of juz numbers that were already finished and a list of juz numbers that were succesfully finished.',
        operation_id='juz_finish',
    )
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
                    
                    data = {'message':'Juz and Hatm completed succesfully'}
                    return Response(data=data, status=status.HTTP_200_OK)
                else:
                    data = {'message':'All Juzs are not completed'}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                juz.status = 'completed'
                juz.save()

                data = {'message':'Juz completed succesfully'}
            return Response(data=data, status=status.HTTP_200_OK)
        
        else:
            data = {'message':'You are not the owner of this juz'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
