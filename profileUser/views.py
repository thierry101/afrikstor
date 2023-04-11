from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from authentication.models import User
from backend.regex import checkUpdateField, updateEmailField, updatePassword
import json

from handleCart.models import Order, ShippingAdress

# Create your views here.


@login_required(login_url='authentication:loginTempl')
def indexProfile(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(
            user_id=request.user.id, complete=True).order_by('-updated')
        addresses = ShippingAdress.objects.filter(user_id=request.user.id)
        address = ShippingAdress.objects.filter(
            user_id=request.user.id, default=True).first()
        infoUsr = User.objects.filter(id=request.user.id).first()
        context = {
            'orders': orders,
            'addresses': addresses,
            'address': address,
            'infoUsr': infoUsr,
        }

        return render(request, 'profile/index.html', context)


def getCommand(request, pk):
    order = Order.objects.filter(id=pk).first()
    orders = json.loads(order.commandProducts)

    return JsonResponse({'success': orders, 'bigTotal': order.newTotal}, safe=False, status=200)


def EditProfile(request):
    if request.user.is_authenticated and request.method == 'POST':
        user = User.objects.filter(id=request.user.id).first()
        errors = {}
        data = request.POST
        name = checkUpdateField(data['name'])
        surname = checkUpdateField(data['surname'])
        email = updateEmailField('email', data['email'], errors)
        password = updatePassword(request, 'password1', 'password2',
                                  data['oldPass'], data['password1'], data['password1'], 8, 'oldPassword', errors)
        if len(errors) == 0:
            if not name and not surname and not email and not password:
                return JsonResponse('nothing', status=200, safe=False)
            else:
                if name:
                    user.first_name = surname
                if surname:
                    user.last_name = name
                if email:
                    user.email = email
                if password:
                    user.set_password(password)
                user.save()
                return JsonResponse('success', status=200, safe=False)
        else:
            return JsonResponse(errors, status=400, safe=False)


def reserPassword(request, token):

    return render(request, 'authentication/reset.html')
