import base64
import datetime
import random
import string
from django.conf import settings
from django.db import transaction
from django.http import Http404, JsonResponse
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, exceptions
from authentication.api.serializers import UserSerializer
from authentication.authentication import JWTAuthentication, create_access_token, create_refresh_token, decode_refresh_token
from authentication.models import ActivationCode, Reset, User, UserToken
from django.shortcuts import get_object_or_404, redirect
from django.core.files.base import ContentFile
from django.conf import settings

from backend.regex import checkExtensionImgUpdate, checkLenOfField, checkPhoneError, checkStatus, id_generator, setEmailError, setPasswordError, updatePhone
from backend.utils import sendMessage
from settingSite.models import SettingSite

debug_flag = settings.DEBUG


class RegisterAPIVIew(APIView):
    # authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated & AdminPermissions]

    def get(self, request):
        users = User.objects.all().order_by('-updated')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        data = request.data
        errors = {}
        role = ''
        statut = False
        appr = []
        first_name = checkLenOfField(
            'first_name', data['first_name'], 3, errors)
        last_name = checkLenOfField('last_name', data['last_name'], 3, errors)
        email = setEmailError('email', data['email'], errors)
        password = setPasswordError('password', 'password_confirm',
                                    data['password'], data['password_confirm'], 8, errors)
        types = data['type']
        if 'approve' in data:
            appr = data['approve']
        checkEmailExist = User.objects.filter(email=email)
        if appr == 'false':
            errors['approve'] = 'Veuillez valider les conditions de confifentialité'
        else:
            appr = True
        if checkEmailExist.exists():
            errors['email'] = 'Cet email existe déjà'
        if types == 'Client':
            role = data['type']
            statut = True
        else:
            if data['statut'] == None:
                statut = False
            else:
                statut = True
            role = checkLenOfField('role', data['type'], 2, errors) or types

        if len(errors) == 0:
            if types == 'CLient':
                user = User.objects.create_user(
                    first_name=first_name, last_name=last_name, approve=appr, email=email, is_email_verified=True, password=password, role=types, statut=statut)
                user.save()
            else:
                user = User.objects.create_user(first_name=first_name, is_email_verified=True, last_name=last_name, email=email,
                                                password=password, approve=appr, statut=statut, role=role)
                user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        user = get_object_or_404(User, pk=int(pk))
        return user

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, pk):
        user = self.get_object(pk)
        errors = {}
        if request.method == 'PUT':
            data = request.data
            # **************** to edit admin info user in admin template **************************
            if 'information' in data:
                data = data['data']
                first_name = checkLenOfField(
                    'first_name', data['first_name'], 3, errors)
                last_name = checkLenOfField(
                    'last_name', data['last_name'], 3, errors)
                email = setEmailError('email', data['email'], errors)
                role = checkLenOfField('role', data['type'], 2, errors)
                statut = checkStatus(data['statut'])
                if len(errors) == 0:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.statut = statut
                    user.role = role
                    user.save()
                    serializer = UserSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            elif 'password' in data:
                # **************** to edit admin password user in admin template **************************
                data = data['data']
                password = setPasswordError('password', 'password_confirm',
                                            data['password'], data['password_confirm'], 8, errors)
                user = User.objects.filter(email=data['email']).first()
                if len(errors) == 0:
                    user.set_password(password)
                    user.save()
                    return Response({
                        'message': 'success'
                    })
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

                # **************** to edit admin status user **************************
            elif 'statut' in data:
                statut = data['data']
                user.statut = statut
                user.save()
                return Response({'message': 'success'}, status=status.HTTP_200_OK)

            # **************** to edit image user profile in profileUser template **************************
            elif 'profileImg' in data:
                data = data['data']
                nameMainImg = checkExtensionImgUpdate(
                    'image', data['image'], 'name', 'file', user.image, errors)
                if len(errors) == 0:
                    slug = id_generator()
                    if data['image']['name'] != '':
                        format, imgstr = data['image']['file'].split(
                            ';base64,')
                        # You can save this as file instance.
                        data = ContentFile(base64.b64decode(imgstr),
                                           name=str(slug)+str(nameMainImg))
                        user.image = data
                        user.save()
                    serializer = UserSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

                # **************** to edit info user in profileUser template **************************
            elif 'profileInfo' in data:
                data = data['data']
                name = checkLenOfField('name', data['name'], 1, errors)
                surname = checkLenOfField(
                    'surname', data['surname'], 1, errors)
                phone = updatePhone('phone', data['phone'], errors)
                mobileMoney = updatePhone(
                    'mobileMoney', data['mobileMoney'], errors)
                if len(errors) == 0:
                    user.first_name = surname
                    user.last_name = name
                    user.phone = phone
                    user.accountMoney = mobileMoney
                    user.save()
                    serializer = UserSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            # **************** to edit password user in profileUser template **************************
            elif 'profilePassword' in data:
                data = data['data']
                password = data['password1']
                if password == '':
                    errors['password'] = "Veuillez renseigner ce champ"
                if password and user and not user.check_password(password):
                    errors['password'] = "Mauvais mot de passe"
                else:
                    newPassword = setPasswordError('password2', 'password3',
                                                   data['password2'], data['password3'], 8, errors)
                if len(errors) == 0:
                    user.set_password(newPassword)
                    user.save()
                    return Response({'message': 'success'}, status=status.HTTP_200_OK)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginAPIView(APIView):
    # ici non devons verifier si l'email a ete verifie en passant statut a true avec de permettre
    # que l'on se logue
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        errors = {}

        user = User.objects.filter(email=email).first()
        if user and not user.statut:
            errors['login'] = 'Vous ne pouvez pas utiliser ces identifiants'
        if user and not user.is_email_verified:
            errors['activate'] = 'Consultez votre boite email pour activer votre compte'
        if user is None:
            errors['login'] = "Identifiants invalids"
        if user and not user.check_password(password):
            errors['login'] = "Identifiants invalids"

        if len(errors) == 0:
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)
            UserToken.objects.get_or_create(
                user_id=user.id, token=refresh_token, expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=7))
            response = Response()
            response.data = {
                'token': access_token,
                'refresh_token': refresh_token
            }
            return response
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.data['token']
        id = decode_refresh_token(refresh_token)

        if not UserToken.objects.filter(user_id=id, token=refresh_token, expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)).exists():
            raise exceptions.AuthenticationFailed("Non authentifié")
        access_token = create_access_token(id)
        return Response({'token': access_token})


class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data['token']
        # on supprime le refresh token afin d'eviter qu'il soit utilise par un tier
        UserToken.objects.filter(token=refresh_token).delete()
        response = Response()
        response.data = {
            'message': 'success'
        }
        return response


class ForgotAPIView(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        typeUser = data['type'] if 'type' in data else 'other'
        # typeUser = data['type']
        path = f"{ request.scheme }://{ request.META.get('HTTP_HOST') }"
        if debug_flag:
            urlFrotend = 'http://localhost:4200'
        else:
            urlFrotend = 'https://afrikstor.ink'
            # urlFrotend = 'admin.afrikstor.com'
        errors = {}
        setting = SettingSite.objects.get(state=True)
        logo = setting.logo
        url = ''
        if email == "":
            errors['email'] = "Veuillez entrer une adresse email"
        else:
            user = User.objects.filter(email=email)
            if not user.exists():
                errors['email'] = "Cet utilisateur n'existe pas"
        if len(errors) == 0:
            token = "".join(random.choice(string.ascii_lowercase +
                                          string.digits) for _ in range(10))
            Reset.objects.create(email=email, token=token)
            if typeUser == 'Client':
                url = path + '/reset/' + token
            else:
                url = urlFrotend + "/reset/" + token

            sendMessage('Réinitialiser votre mot de passe', 'emails/resetPassword.html',
                        {'setting': setting, 'path': path, 'logo': logo, 'url': url},  settings.EMAIL_HOST_USER, (email,))
            # send_mail(
            #     subject="Reset your password",
            #     message='Click <a href="%s">here</a> to reset your password' % url,
            #     from_email=settings.EMAIL_HOST_USER,
            #     recipient_list=[email, ]
            # )

            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class ResetAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        errors = {}

        reset_password = Reset.objects.filter(token=data['token']).first()
        if not reset_password:
            errors['link'] = "Lien invalide"
        else:
            password = setPasswordError('password', 'password_confirm',
                                        data['password'], data['password_confirm'], 8, errors)
            user = User.objects.filter(email=reset_password.email).first()
            if not user:
                errors['users'] = "Cet utilisateur n'existe pas"
        if len(errors) == 0:
            user.set_password(password)
            user.save()
            Reset.objects.get(token=data['token']).delete()
            return Response({
                'message': 'success'
            })
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


def checkActivationCode(request, code):

    try:
        userActiv = ActivationCode.objects.filter(code=code)
    except ActivationCode.DoesNotExist:
        raise Http404
    if userActiv.exists():
        usr = ActivationCode.objects.get(code=code)
        usrAct = User.objects.get(pk=usr.user.id)
        usrAct.is_email_verified = True
        usrAct.statut = True
        usrAct.save()
        ActivationCode.objects.get(code=code).delete()
        if debug_flag:
            return redirect('http://127.0.0.1:4200/login')
        else:
            return redirect('https://afrikstor.ink/')
    else:
        return JsonResponse('Ce lien est expiré', status=400, safe=False)


# ************************ class to register SELLER **********************************
class RegisterSellerAPIVIew(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all().order_by('-updated')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        data = request.data
        errors = {}
        nameShop = checkLenOfField('nameShop', data['nameShop'], 3, errors)
        first_name = checkLenOfField(
            'first_name', data['first_name'], 3, errors)
        last_name = checkLenOfField('last_name', data['last_name'], 3, errors)
        city = checkLenOfField('city', data['city'], 3, errors)
        country = checkLenOfField('country', data['country'], 3, errors)
        email = checkLenOfField('email', data['email'], 3, errors)
        phone = checkPhoneError('phone', data['phone'], errors)
        moneyPhone = checkPhoneError('moneyPhone', data['moneyPhone'], errors)
        password = setPasswordError('password', 'password_confirm',
                                    data['password'], data['password_confirm'], 8, errors)
        checkUsr = User.objects.filter(email=email)
        approve = data['approve']
        if approve == False:
            errors['approve'] = 'Veuillez accepter notre politique de vente'
        else:
            approve == True
        if checkUsr.exists():
            errors['email'] = 'Cet email existe déjà'
        else:
            pass
        typeUser = data['type']
        if len(errors) == 0:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, nameShop=nameShop,
                                            city=city, country=country, phone=phone, accountMoney=moneyPhone, email=email, password=password,
                                            role=typeUser, approve=approve)
            user.save()
            code = ActivationCode.objects.create(user=user)
            code.save()
            path = f"{ request.scheme }://{ request.META.get('HTTP_HOST') }"
            setting = SettingSite.objects.filter(state=True).first()
            logo = setting.logo if setting else ''
            sendMessage('Activez votre compte', 'emails/activation.html', {
                'user': user,
                'domain': path,
                'code': code.code,
                'setting': setting,
                'logo': logo,
            }, settings.EMAIL_HOST_USER, (user.email, ))
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
