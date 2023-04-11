from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction

from authentication.authentication import JWTAuthentication
from authentication.permissions import AdminPermissions
from contactAndAbout.api.serializers import MessageSerializer
from contactAndAbout.models import MessageContact


class MessageAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get(self, request):
        messages = MessageContact.objects.all().order_by('-updated')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get_object(self, pk):
        message = get_object_or_404(MessageContact, id=int(pk))
        return message

    @transaction.atomic
    def put(self, request, pk):
        message = self.get_object(pk)
        errors = {}
        if request.method == 'PUT':
            data = request.data
            state = data['newState']
            if data['state']:
                message.statut = state
                message.save()
            return Response('updated', status=status.HTTP_200_OK)
