import json
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404

from authentication.authentication import JWTAuthentication
from authentication.models import User
from authentication.permissions import AdminPermissions
from backend.regex import checkDateAndCompare, checkIdSelected, checkLenOfField, checkStartWith, checkStatus
from backend.utils import checkPaymentMethod, sendMessage
from handleCart.api.serializers import CouponSerializer, OrderSerializer
from handleCart.models import CouponGerate, Order
from authentication.api.serializers import UserSerializer
from settingSite.models import SettingSite


class CouponAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get(self, request):
        coupons = CouponGerate.objects.all().order_by('active')
        serializer = CouponSerializer(coupons, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic()
    def post(self, request):
        errors = {}
        if request.method == 'POST':
            data = request.data
            reduction = checkLenOfField(
                'reduction', str(data['reduction']), 1, errors)
            statut = checkStatus(data['statut'])
            userid = checkIdSelected(
                'userid', data['userid'], 'une commande', errors)
            code = checkStartWith('code', data['code'], 'AfStor', errors)
            duration = checkDateAndCompare(
                'startDate', 'endDate', data['dateBegin'], data['dateEnd'], errors)
            if len(errors) == 0:
                startDate = duration['startDate']
                endDate = duration['endDate']
                user = User.objects.get(id=int(userid))
                coupon = CouponGerate.objects.create(user_id=int(
                    userid), code=code, valid_from=startDate, valid_to=endDate, discount=reduction, active=statut)
                coupon.save()
                sendMessage('Bon de réduction', 'emails/discount.html', {
                    'code': code,
                    'user': user,
                    'reduction': reduction,
                    'expiration': coupon.valid_to,

                }, settings.EMAIL_HOST_USER, (user.email,))
                serializer = CouponSerializer(coupon)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            pass


class UserClientAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get(self, request):
        users = User.objects.filter(role__iregex='client')
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get(self, request):
        orders = Order.objects.filter(complete=True).order_by('-updated')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get_object(self, pk):
        order = get_object_or_404(Order, nberInvoice=(pk))
        return order

    @transaction.atomic
    def put(self, request, pk):
        order = self.get_object(pk)
        errors = {}

        if request.method == 'PUT':
            path = f"{ request.scheme }://{ request.META.get('HTTP_HOST') }"
            setting = SettingSite.objects.get(state=True)
            payment = checkPaymentMethod(
                order.paymentMethod, setting.mtnMoney, setting.orangeMoney)
            logo = setting.logo
            data = request.data
            if data['setAmout']:
                deliveryAmt = data['amount']
                order.priceDelivery = deliveryAmt
                order.status = 'en cours'
                order.save()
                serializer = OrderSerializer(order)

                if order.user:
                    sendMessage('Facture No: '+order.nberInvoice, 'emails/invoice.html', {
                        'items': json.loads(order.commandProducts), 'order': order,
                        'path': path, 'logo': logo, 'setting': setting, 'payment': payment,
                        'method': order.paymentMethod,
                    }, settings.EMAIL_HOST_USER, (request.user.email,))
                else:
                    infoUser = json.loads(order.infoAnonUser)
                    sendMessage('Facture No: '+order.nberInvoice, 'emails/invoice.html', {
                        'items': json.loads(order.commandProducts),
                        'order': order, 'payment': payment,
                        'path': path, 'infoUser': infoUser, 'logo': logo,
                        'method': order.paymentMethod,
                        'setting': setting,
                    }, settings.EMAIL_HOST_USER, (request.user.email,))

                # change statut send email
                # apres le status en cours c'est paye ensuite livre et a livre on passe le order delivered a true
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                stat = data['newStat']
                order.status = stat
                order.save()
                return Response('updated', status=status.HTTP_200_OK)
