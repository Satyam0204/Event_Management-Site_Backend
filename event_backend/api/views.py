from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import * 
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
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