from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('',viewRoutes, name='viewRoutes'),
    path('register/',Register.as_view(),name='register'),
    path('login/',  TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('newevent/',CreateEvent),
    path('getevents/',getEvents),
    path('getevent/<str:pk>/',getSpecificEvent),
    ]