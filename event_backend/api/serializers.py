from dataclasses import field
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','password']
    
    def create(self, validated_data):
        user=User.objects.create(email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields='__all__'


