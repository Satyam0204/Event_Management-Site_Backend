from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import * 
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone


from rest_framework import status


@api_view(['GET'])
def viewRoutes(request):
    routes=[
            {
            'endpoint':'/api/',
            'method':'GET',
            'desc':'view all routes',
            },
            {
            'endpoint':'/api/register/',
            'method':'POST',
            'desc':'registerisng user'
            },
            {
            'endpoint':'/api/login/',
            'method':'POST',
            'desc':'getthing jwt token'
            },

            {'endpoint':'/api/token/refresh/',
            'method':'POST',
            'desc':'refreshing access token using refresh token'},

            {'endpoint':'/api/newevent/',
            'method':'POST',
            'desc':'creating new event with the authozised user'},

            {'endpoint':'/api/getevents/',
            'method':'GET',
            'desc':'get all the past, live and upcoming events specified'},

            {'endpoint':"/api/getevent/<id>",
            'method':'GET',
            'desc':'get a specific event with event.id=id with average rating and no of interested users'},

            {'endpoint':"/api/rateevent/<id>",
            'method':"['POST','PUT']",
            'desc':'rate or update rating a specific event with event.id=id between 1 to 5'},

            {'endpoint':"/api/showinterest/<id>",
            'method':'POST',
            'desc':'show interest to a specific event with event.id = id between 1 to 5'},


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
        event=Event.objects.create(name=data['name'],desc=data['desc'],start_date=data['start_date'],end_date=data['end_date'],host=user)
        serializers=EventSerializer(event,many=False)
        return Response(serializers.data)
    else:
        raise ValueError("start date must be earlier than end date")


#getting all the upcoming , live and upcoming events
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEvents(request):
    time=timezone.now()
    print(time)
    upcomingevents=[]
    liveevents=[]
    pastevents=[]
    events=Event.objects.all()
    for event in events:
        if (time<event.start_date and time<event.end_date):
            print(event.start_date)
            upcomingevents.append(event)

        elif(time>=event.start_date and time<event.end_date):
            liveevents.append(event)
        else:
            pastevents.append(event)
    upc_serializers=EventSerializer(upcomingevents,many=True)

    le_serializers=EventSerializer(liveevents,many=True)
    pe_serializers=EventSerializer(pastevents,many=True)
    response={"upcoming_events":upc_serializers.data,"live_events":le_serializers.data,"past_events":pe_serializers.data}

    return Response(response)

#getthing specific event with id with avg rating and total interested users
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSpecificEvent(request,pk):
    event=Event.objects.get(id=pk)
    serializers=EventSerializer(event)
    response=serializers.data
    response['avg_rating']=event.avg_rating()
    response['total_interested_users']=event.interested_count()
    return Response(response)

#rate the event
@api_view(['POST','PUT'])
@permission_classes([IsAuthenticated])
def rate(request,pk):
    event=Event.objects.get(id=pk)
    user= request.user
    data=request.data
    if(not Rating.objects.filter(user=user,event=event).exists()):
        Rating.objects.create(event=event,user=user,rating=data['rating'])
        return Response("You rated "+event.name+" with rating "+data['rating'])
    else:
        Rating.objects.update(event=event,user=user,rating=data['rating'])
        return Response("You updated rating "+event.name+" with rating "+data['rating'])

#show interest to the event
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def showInterest(request,pk):
    event=Event.objects.get(id=pk)
    user=request.user
    Interest.objects.create(event=event,user=user)
    return Response("You showed interest to"+event.name)