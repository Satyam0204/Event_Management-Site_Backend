from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import * 
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import status


@api_view(['GET'])
def viewRoutes(request):
    routes=[
            {
            'endpoint':'viewRoutes',
            'desc':'view all routes',

            },
    ]

    return Response(routes)

    
class Register(APIView):
    @classmethod
    def post(self, request):
        userdata=request.data
        serialize=UserSerializer(data=userdata)



        if (not serialize.is_valid()):
            
            return Response(serialize.errors)
        serialize.save()
        user=User.objects.get(email=serialize.data['email'])

        refresh = RefreshToken.for_user(user)
        return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateEvent(request):
    user=request.user
    data=request.data
    if(data['start_date']<=data['end_date']):
        event=Event.objects.create(name=data['name'],desc=data['desc'],start_date=data['start_date'],end_date=data['end_date'],author=user)
        serializers=EventSerializer(event,many=False)
        return Response(serializers.data)
    else:
        raise ValueError("start date must be earlier than end date")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEvents(request):
    events=Event.objects.all()

    serializers=EventSerializer(events,many=True)

    return Response(serializers.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSpecificEvent(request,pk):
    event=Event.objects.get(id=pk)
    serializers=EventSerializer(event)
    response=serializers.data
    response['avg_rating']=event.avg_rating()
    return Response(response)
