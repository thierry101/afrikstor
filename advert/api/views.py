import base64
from turtle import title
from rest_framework.views import APIView
from django.db import transaction
from advert.api.serializers import AdvertSerializer
from advert.models import Advert
from authentication.authentication import JWTAuthentication
from authentication.permissions import AdminPermissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from backend.regex import checkDateAndCompare, checkExtensionImg, checkExtensionImgUpdate, checkLenOfField, checkStatus, convertToInt, deleteOneImg


class AdvertAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get(self, request):
        advert = Advert.objects.all().order_by('-updated')
        serializer = AdvertSerializer(advert, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        data = request.data
        errors = {}
        title = checkLenOfField('title', data['title'], 2, errors)
        brand_id = convertToInt(
            'brand_id', data['brand_id'], 'une marque', errors)
        statut = data['statut']
        nameImg = checkExtensionImg(
            'banner', data['banner'], 'name', 'file', errors)
        duration = checkDateAndCompare(
            'startDate', 'endDtate', data['beginDate'], data['endDate'], errors)

        if len(errors) == 0:
            startDate = duration['startDate']
            endDate = duration['endDate']

            advert = Advert.objects.create(title=title, brand_id=int(
                brand_id), begin_date=startDate, end_date=endDate, statut=statut)
            advert.save()

            # save main img
            format, imgstr = data['banner']['file'].split(';base64,')
            # You can save this as file instance.
            advert.img = ContentFile(
                base64.b64decode(imgstr), name=str(nameImg))
            advert.save()
            serializer = AdvertSerializer(advert)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class AdvertEditAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get_object(self, pk):
        advert = get_object_or_404(Advert, pk=int(pk))
        return advert

    @transaction.atomic
    def put(self, request, pk):
        advert = self.get_object(pk)
        errors = {}
        if request.method == 'PUT':
            datas = request.data
            if 'statut' in datas:
                statut = checkStatus(datas['stateAdvert'])
                advert.statut = statut
                advert.save()
                return Response('success', status=status.HTTP_200_OK)
            if 'state' in datas:
                data = datas['data']
                title = checkLenOfField('title', data['title'], 2, errors)
                brand_id = convertToInt(
                    'brand_id', data['brand_id'], 'une marque', errors)
                statut = data['statut']
                duration = checkDateAndCompare(
                    'startDate', 'endDtate', data['beginDate'], data['endDate'], errors)
                if data['banner']['name'] != '':
                    nameImg = checkExtensionImgUpdate(
                        'banner', data['banner'], 'name', 'file', advert.img, errors)
                if len(errors) == 0:
                    startDate = duration['startDate']
                    endDate = duration['endDate']
                    advert.title = title
                    advert.brand_id = int(brand_id)
                    advert.begin_date = startDate
                    advert.end_date = endDate
                    advert.statut = statut
                    advert.save()

                    # save Img
                    if data['banner']['name'] != '':
                        format, imgstr = data['banner']['file'].split(
                            ';base64,')
                        # You can save this as file instance.
                        advert.img = ContentFile(
                            base64.b64decode(imgstr), name=str(nameImg))
                        advert.save()
                    serializer = AdvertSerializer(advert)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        advert = self.get_object(pk)

        deleteOneImg(advert.img)
        advert.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
