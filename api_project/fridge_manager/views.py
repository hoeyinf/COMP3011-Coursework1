from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, status, permissions
from fridge_manager.serializers import *
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class UserProfile(APIView):
    """
    API endpoint for users.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
