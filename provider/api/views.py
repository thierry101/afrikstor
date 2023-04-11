import os

from django.conf import settings
from authentication.api.serializers import UserSerializer
from authentication.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from authentication.permissions import AdminPermissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db import transaction


class ProviderAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get(self, request):
        providers = User.objects.filter(
            role__iregex='vendeur').order_by('-updated') | User.objects.filter(
            role__iregex='seller').order_by('-updated')
        serializer = UserSerializer(providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProviderDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get_object(self, pk):
        provider = get_object_or_404(User, pk=int(pk))
        return provider

    def get(self, request, pk):
        provider = self.get_object(pk)
        serializer = UserSerializer(provider)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, pk):
        provider = self.get_object(pk)
        errors = {}
        if request.method == 'PUT':
            data = request.data

            if 'statut' in data:
                statut = data['data']
                provider.statut = statut
                provider.save()
                return Response({'success': 'success'}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        provider = self.get_object(pk)
        mainImg = "/" + str(provider.image)
        if(mainImg == '/'):
            pass
        else:
            if os.path.exists(settings.MEDIA_ROOT + mainImg):
                os.remove(settings.MEDIA_ROOT + mainImg)
            else:
                pass
            provider.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
