from django.shortcuts import get_object_or_404

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
        queryset = Hatm.objects.filter(is_completed=False, is_published=True)
        serializer = self.serializer_class(queryset, many=True, context={'request':self.get_serializer_context()})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
    serializer_class = HatmSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Hatm.objects.all()
    
    @swagger_auto_schema(
        operation_description='Get list of hatm with specific juzs that taken by user',
        responses={200: HatmSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request':self.get_serializer_context()})
        #filter juzs by user_id if its exists
        data = []
        for hatm in serializer.data:
            juzs = hatm['juz']
            juzs = [juz for juz in juzs if 'user_id' in juz and juz['user_id'] == str(self.request.user.id)]
            hatm['juz'] = juzs
            if len(hatm['juz']) < 1:
                return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            data.append(hatm)
        return Response(data, status=status.HTTP_200_OK)
    

class HatmCreatedViewSet(generics.ListAPIView):
    serializer_class = HatmSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        queryset = Hatm.objects.filter(creator_id=str(request.user.id))
        serializer = self.serializer_class(queryset, many=True, context={'request':self.get_serializer_context()})
        return Response(serializer.data, status.HTTP_200_OK)
    

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
                'already_taken': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                'succesfully_taken': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                'unseccesfully_taken': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
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
            deadline = datetime.datetime.now() + datetime.timedelta(days=days)
            queryset = self.get_queryset()
            taken_juzs = []
            succesfully = []
            unseccesfully = []
            for juz in queryset:
                if juz.type == 'juz':
                    if juz.status == 'free':
                        juz.status = 'in Progress'
                        juz.user_id = request.user
                        juz.deadline = deadline
                        juz.save()
                        succesfully.append(juz.juz_number)
                    else:
                        taken_juzs.append(juz.juz_number)
                else:
                    if is_all_completed(juz.hatm_id):
                        juz.status = 'in Progress'
                        juz.user_id = request.user
                        juz.deadline = deadline
                        juz.save()
                        succesfully.append(juz.juz_number)
                    else:
                        unseccesfully.append(juz.juz_number)
            deadline = deadline.strftime(format='%Y-%m-%d %H:%M:%Sw')
                
            data = {'already_taken': taken_juzs, 'succesfully_taken': succesfully, 'unsuccesfully_taken':unseccesfully, 'deadline': deadline}
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
        if str(juz.user_id) == str(request.user):
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

        if str(juz.user_id) == str(request.user):
            
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
                            create_or_publish_public_hatm(hatm.creator_id)
                    
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


class JoinRequestView(generics.GenericAPIView):
    serializer_class = JoinHatmRequestSerializer
    queryset = JoinRequest.objects.all()

    def post(self, request):
        hatm_id = request.data.get('hatm')
        user_id = request.data.get('user')
        hatm = Hatm.objects.get(id=hatm_id)

        if request.user in hatm.members.all():
            return Response({'message': 'You are already a member of this hatm.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if hatm.is_completed:
            return Response({'message': 'This hatm is completed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if hatm.is_public:    
            hatm.members.add(request.user)
            hatm.save()
            return Response({'message': 'You joined to this hatm succesfully!'}, status=status.HTTP_200_OK)
        else:
            if JoinRequest.objects.filter(hatm=hatm, user=request.user):
                joinRequest = JoinRequest.objects.get(hatm=hatm, user=request.user)
                
                if joinRequest.status == 'pending':
                    return Response({'message': 'You already sent a request for this hatm.'}, status=status.HTTP_400_BAD_REQUEST)
                elif joinRequest.status == 'rejected':
                    joinRequest.status = 'pending'
                    joinRequest.save()
                else:
                    return Response({'message': 'You are already a member of this hatm.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(hatm=hatm, user=request.user, status='pending')
            return Response({'message': 'Your request has been sent succesfully!'}, status=status.HTTP_200_OK)
        

class PendingRequest(generics.ListAPIView):
    serializer_class = PendingRequestsSerializer

    #select JoinRequest objects that status=pending and hatm creator id = user.id
    def get_queryset(self):
        user = self.request.user
        return JoinRequest.objects.filter(status='pending', hatm__creator_id=user.id)
    

class ApproveRejectRequestView(generics.GenericAPIView):
    serializer_class = RequestsSerializer
    queryset = JoinRequest.objects.all()

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        },
        request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['rejected', 'approved'],
                    description='Status',
                ),
            },
            required=['status'],
        ),
        operation_description='This view respondes to request to join hatm.',
        operation_id='respond_to_request',
    )
    def patch(self, request, pk, *args, **kwargs):
        join_request = self.get_object()
        serializer = self.get_serializer(join_request, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        hatm = join_request.hatm
        
        if hatm.creator_id == request.user:
            if join_request.status != 'pending':
                return Response(data={'message': 'You have already responded to this request!'}, status=status.HTTP_400_BAD_REQUEST)
            
            if serializer.validated_data['status'] == 'approved':
                hatm.members.add(join_request.user)
            
            serializer.save()
        
        else:
            return Response(data={'message': 'You are not owner of this hatm'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)