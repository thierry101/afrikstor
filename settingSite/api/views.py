import base64
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.core.files.base import ContentFile

from authentication.authentication import JWTAuthentication
from authentication.permissions import AdminPermissions
from backend.regex import checkExtensionImg, checkExtensionImgUpdate, checkUpdateField, id_generator, updateEmailField, updatePhone
from settingSite.api.serializers import ConfidentialityAndRuleSerializer, SettingSiteSerializer
from settingSite.models import ConfidentialityAndRule, SettingSite


class SettingSiteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = SettingSiteSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get(self, request):
        setting = SettingSite.objects.all().first()
        serializer = SettingSiteSerializer(setting)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request):
        setting = SettingSite.objects.all().first()
        data = request.data
        errors = {}
        if 'profileInfo' in data:
            data = data['data']
            phone = updatePhone('phone', data['phone'], errors)
            mtnMoney = updatePhone('mtnMoney', data['mtnMoney'], errors)
            orangeMoney = updatePhone(
                'orangeMoney', data['orangeMoney'], errors)
            email = updateEmailField('email', data['email'], errors)
            localisation = checkUpdateField(data['localisation'])
            whatsapp = checkUpdateField(data['link_whatsapp'])
            facebook = checkUpdateField(data['link_facebook'])
            messenger = checkUpdateField(data['link_messenger'])
            if len(errors) == 0:
                if setting == None:
                    setting = SettingSite.objects.get_or_create(email=email, phone=phone, localisation=localisation,
                                                                link_whatsapp=whatsapp, link_facebook=facebook, link_messenger=messenger)
                    serializer = SettingSiteSerializer(setting)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    setting.email = email
                    setting.phone = phone
                    setting.mtnMoney = mtnMoney
                    setting.orangeMoney = orangeMoney
                    setting.localisation = localisation
                    setting.link_whatsapp = whatsapp
                    setting.link_facebook = facebook
                    setting.link_messenger = messenger
                    setting.save()
                    serializer = SettingSiteSerializer(setting)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        elif 'siteLogo' in data:
            data = data['data']
            if setting == None:
                nameMainImg = checkExtensionImg(
                    'logo', data['logo'], 'name', 'file', errors)
                if len(errors) == 0:
                    slug = id_generator()
                    format, imgstr = data['logo']['file'].split(';base64,')
                    # You can save this as file instance.
                    data = ContentFile(base64.b64decode(
                        imgstr), name=str(slug)+str(nameMainImg))
                    setting = SettingSite.objects.get_or_create(logo=data)
                    serializer = SettingSiteSerializer(setting)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                nameMainImg = checkExtensionImgUpdate(
                    'logo', data['logo'], 'name', 'file', setting.logo, errors)
                if len(errors) == 0:
                    slug = id_generator()
                    if data['logo']['name'] != '':
                        format, imgstr = data['logo']['file'].split(';base64,')
                        # You can save this as file instance.
                        data = ContentFile(base64.b64decode(imgstr),
                                           name=str(slug)+str(nameMainImg))
                        setting.logo = data
                        setting.save()
                    serializer = SettingSiteSerializer(setting)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        elif 'siteFavIco' in data:
            data = data['data']
            if setting == None:
                nameMainImg = checkExtensionImg(
                    'fav_icon', data['fav_icon'], 'name', 'file', errors)
                if len(errors) == 0:
                    slug = id_generator()
                    format, imgstr = data['fav_icon']['file'].split(';base64,')
                    # You can save this as file instance.
                    data = ContentFile(base64.b64decode(
                        imgstr), name=str(slug)+str(nameMainImg))
                    setting = SettingSite.objects.get_or_create(fav_icon=data)
                    serializer = SettingSiteSerializer(setting)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                nameMainImg = checkExtensionImgUpdate(
                    'fav_icon', data['fav_icon'], 'name', 'file', setting.fav_icon, errors)
                if len(errors) == 0:
                    slug = id_generator()
                    if data['fav_icon']['name'] != '':
                        format, imgstr = data['fav_icon']['file'].split(
                            ';base64,')
                        # You can save this as file instance.
                        data = ContentFile(base64.b64decode(imgstr),
                                           name=str(slug)+str(nameMainImg))
                        setting.fav_icon = data
                        setting.save()
                    serializer = SettingSiteSerializer(setting)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# ******************** to get confidentiality **********************************
class GetConfidentialityAndRuleAPIView(APIView):
    serializer_class = ConfidentialityAndRuleSerializer

    def get(self, request):
        configRule = ConfidentialityAndRule.objects.all().first()
        serializer = ConfidentialityAndRuleSerializer(configRule)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfidentialityAndRuleAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ConfidentialityAndRuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & AdminPermissions]

    def get(self, request):
        configRule = ConfidentialityAndRule.objects.all().first()
        serializer = ConfidentialityAndRuleSerializer(configRule)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request):
        configRule = ConfidentialityAndRule.objects.all().first()
        data = request.data
        if 'confidentiality' in data:
            confidentiality = data['data']
            if configRule == None:
                confidRul = ConfidentialityAndRule.objects.get_or_create(
                    confidentiality=confidentiality)
                return Response({'success': 'success'}, status=status.HTTP_200_OK)
            else:
                configRule.confidentiality = confidentiality
                configRule.save()
                return Response({'success': 'success'}, status=status.HTTP_200_OK)

        elif 'ruleSeller' in data:
            rulerSeller = data['data']
            if configRule == None:
                confidRul = ConfidentialityAndRule.objects.get_or_create(
                    rulerSeller=rulerSeller)
                return Response({'success': 'success'}, status=status.HTTP_200_OK)
            else:
                configRule.rulerSeller = rulerSeller
                configRule.save()
                return Response({'success': 'success'}, status=status.HTTP_200_OK)
        elif 'ruleBuyer' in data:
            rulerBuyer = data['data']
            print("the ruler buyer", rulerBuyer)
            if configRule == None:
                confidRul = ConfidentialityAndRule.objects.get_or_create(
                    rulerBuyer=rulerBuyer)
                return Response({'success': 'success'}, status=status.HTTP_200_OK)
            else:
                configRule.rulerBuyer = rulerBuyer
                configRule.save()
                return Response({'success': 'success'}, status=status.HTTP_200_OK)
