import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from backend.regex import checkLenOfField, checkPayment, checkPhoneError, checkStartWith, generateNumber, gererateOrderNber, setEmailError
from backend.utils import getTotalPrice, removekey
from django.core import serializers
from handleCart.api.serializers import ShippingAdressSerializer
from handleCart.models import CouponGerate, OrderItem, Order, ShippingAdress
from registerProduct.models import RegisterProduct

# Create your views here.


@transaction.atomic
def AddToCart(request):
    if request.is_ajax():
        data = request.POST
        idProd = data['idProd']
        color = data['color'] if data['color'] != 'undefined' else None
        size = data['size'] if data['size'] != 'undefined' else None
        qte = data['qte']
        price = 0
        total = 0
        bigTotal = 0
        product = RegisterProduct.objects.get(pk=idProd)
        path = f"{ request.scheme }://{ request.META.get('HTTP_HOST') }"
        title = product.title
        imgProd = path + product.mainImg.url
        if product.sold_price:
            price = product.sold_price
        else:
            price = product.price
        if request.user.is_authenticated:
            order_item = OrderItem.objects.filter(user_id=request.user.id,
                                                  product_id=int(idProd), color=color, size=size)
            if order_item.exists():
                order_item = OrderItem.objects.get(
                    product_id=int(idProd), color=color, size=size)
                order_item.quantity += int(qte)
                total = int(order_item.quantity) * float(price)
                order_item.total = total
                order_item.save()
                order = Order.objects.filter(
                    user_id=request.user.id, complete=False).first()
                items = order.items.all()
                bigTotal = getTotalPrice(Order, request)
                data = {'message': 'updated', 'bigTotal': bigTotal,
                        'items': serializers.serialize('json', items)}
                order.newTotal = bigTotal
                order.save()
                return JsonResponse(data, safe=False)
            else:
                total = int(qte) * float(price)
                order_item, created = OrderItem.objects.get_or_create(user_id=request.user.id,
                                                                      product_id=int(idProd), pathImg=imgProd, title=title, color=color, size=size, price=price, quantity=qte, total=total)

            order_qs = Order.objects.filter(
                user_id=request.user.id, complete=False)
            if order_qs.exists():
                order = order_qs[0]
                order.items.add(order_item)
            else:
                order = Order.objects.create(user=request.user)
                order.items.add(order_item)
            items = order.items.all()
            bigTotal = getTotalPrice(Order, request)
            data = {'message': 'success added', 'bigTotal': bigTotal,
                    'nberItems': items.count(), 'items': serializers.serialize('json', items)}
            order.newTotal = bigTotal
            order.save()
            return JsonResponse(data, safe=False)
        else:
            # del request.session['cartData']
            cart_p = {}
            cart_data = {}
            bigTotal = 0
            prod = RegisterProduct.objects.filter(pk=int(idProd)).first()
            pathImg = RegisterProduct.objects.get(pk=int(idProd)).mainImg.url
            cart_p[str(idProd)] = {
                'title': title,
                'qte': int(qte),
                'price': float(price),
                'color': color,
                'size': size,
                'subTotal': int(qte) * float(price),
                'path': str(pathImg),
                'phoneProvider': prod.user.phone,
                'emailProvider': prod.user.email
            }
            if 'cartData' in request.session:
                if str(idProd) in request.session['cartData']:
                    cart_data = request.session['cartData']
                    cart_data[str(idProd)]['qte'] = int(
                        cart_data[str(idProd)]['qte']) + int(qte)
                    cart_data[str(idProd)]['subTotal'] = cart_data[str(
                        idProd)]['qte'] * cart_data[str(idProd)]['price']
                    cart_data.update(cart_data)
                    request.session['cartData'] = cart_data
                    for element in request.session['cartData']:
                        bigTotal += request.session['cartData'][element]['subTotal']
                    return JsonResponse({'message': 'updated', 'data': cart_data, 'count': len(cart_data), 'bigTotal': bigTotal})
                else:
                    cart_data = request.session['cartData']
                    cart_data.update(cart_p)
                    request.session['cartData'] = cart_data
                for element in request.session['cartData']:
                    bigTotal += request.session['cartData'][element]['subTotal']
            else:
                request.session['cartData'] = cart_p
                cart_data = request.session['cartData']
                bigTotal = cart_data[str(idProd)]['qte'] * \
                    cart_data[str(idProd)]['price']
            return JsonResponse({'message': 'success', 'data': cart_data, 'count': len(cart_data), 'bigTotal': bigTotal})


def applyCoupon(request):
    errors = {}
    reduction = 0
    discount = 0
    bigTotal = 0
    newBigTotal = 0

    if request.method == 'POST' and request.is_ajax():
        data = request.POST
        valueCoupon = checkStartWith(
            'valueCoupon', data['valCoupon'], 'AfStor', errors)
        coupon = CouponGerate.objects.filter(code=valueCoupon)
        if coupon.exists():
            current_date = datetime.datetime.now().date()
            valid_to = coupon.first().valid_to
            if valid_to < current_date:
                errors['valueCoupon'] = 'Ce coupon est expiré'
            elif coupon.first().active == False:
                errors['valueCoupon'] = 'Ce coupon est déja utilisé'
            else:
                pass
        else:
            pass
        if len(errors) == 0:
            bigTotal = getTotalPrice(Order, request)
            discount = coupon.first().discount
            reduction = float(bigTotal) * float(discount) / 100
            newBigTotal = float(bigTotal) - float(reduction)
            order = Order.objects.get(user_id=request.user.id, complete=False)
            order.reduction = reduction
            order.newTotal = newBigTotal
            order.active = True
            order.save()
            data = {
                'reduction': reduction,
                'newBigTotal': newBigTotal,
            }
            return JsonResponse(data, status=200, safe=False)
        else:
            return JsonResponse(errors, status=400)
    else:
        pass


def viewCart(request):
    allItems = []
    bigTotal = 0
    if not request.user.is_authenticated and 'cartData' in request.session:
        items = request.session['cartData']
        for item in items:
            ite = RegisterProduct.objects.get(id=int(item))
            allItems.append({'product': ite, 'other': items[item]})
            bigTotal += items[item]['subTotal']
        context = {
            'allItems': allItems,
            'bigTotal': bigTotal,
            'viewCart': True,
        }
    else:
        context = {
            'viewCart': True,
        }
    return render(request, 'shop/viewCart.html', context)


@transaction.atomic
def updateQte(request):
    bigTotal = 0
    data = request.POST
    idProd = data['idProd']
    qte = data['qte']
    if request.is_ajax() and request.user.is_authenticated:
        idOrder = data['idOrder']
        if request.user.is_authenticated:
            order = Order.objects.filter(
                user_id=request.user.id, complete=False, id=idOrder)
            product = order[0].items.get(id=int(idProd))
            product.quantity = qte
            product.save()
            product.total = int(product.quantity) * float(product.price)
            product.save()
            bigTotal = getTotalPrice(Order, request)
            produc = order[0].items.filter(id=int(idProd))
            serializer = serializers.serialize('json', produc)
            return JsonResponse({'data': serializer, 'bigTotal': bigTotal}, safe=False)
    else:
        if 'cartData' in request.session:
            cart_data = request.session['cartData']
            cart_data[str(idProd)]['qte'] = int(qte)
            cart_data[str(idProd)]['subTotal'] = cart_data[str(
                idProd)]['qte'] * cart_data[str(idProd)]['price']
            cart_data.update(cart_data)
            request.session['cartData'] = cart_data
            for element in request.session['cartData']:
                bigTotal += request.session['cartData'][element]['subTotal']
            return JsonResponse({'message': 'updated', 'data': cart_data, 'bigTotal': bigTotal})


@transaction.atomic
def delItemFromOrder(request):
    bigTotal = 0
    data = request.POST
    if request.user.is_authenticated and request.is_ajax():
        idOrder = data['idOrder']
        idProd = data['idProd']
        itemDelete = get_object_or_404(OrderItem, id=int(idProd))
        order = Order.objects.get(
            user_id=request.user.id, complete=False, id=int(idOrder))
        order.items.remove(itemDelete)
        itemDelete.delete()
        itemsCount = order.items.all().count()
        bigTotal = getTotalPrice(Order, request)
        data = {
            'success': 'delete',
            'title': itemDelete.product.title,
            'total': bigTotal,
            'itemsCount': itemsCount,
        }
        return JsonResponse(data, safe=False)
    else:
        bigTotal = 0
        datas = {}
        if 'cartData' in request.session:
            cart_data = request.session['cartData']
            newCart = removekey(cart_data, data['idProd'])
            del request.session['cartData']
            request.session['cartData'] = newCart
            cart_data = request.session['cartData']
            itemsCount = len(cart_data)
            for element in request.session['cartData']:
                bigTotal += request.session['cartData'][element]['subTotal']

            datas = {
                'success': 'delete',
                'total': bigTotal,
                'itemsCount': itemsCount,
            }

        return JsonResponse(datas, status=200, safe=False)


def checkoutIndex(request):
    addresses = ShippingAdress.objects.filter(user_id=request.user.id)
    context = {
        'addresses': addresses,
    }
    return render(request, 'shop/checkout.html', context)


@transaction.atomic
def registerAddress(request):
    data = request.POST
    errors = {}
    if request.user.is_authenticated:
        name = data['name']
        surname = data['surname']
        selectDefault = data['idSelectDefault']
        exactAddress = data['exactAddress']
        phone = checkPhoneError('phone', data['phone'], errors)
        country = checkLenOfField('country', data['country'], 2, errors)
        city = checkLenOfField('city', data['city'], 2, errors)
        address = checkLenOfField('address', data['address'], 2, errors)

        if len(errors) == 0:
            if name == '':
                name = request.user.first_name
            if surname == '':
                surname = request.user.last_name
            if selectDefault == 'true':
                selectDefault = True
            else:
                selectDefault = False
            addresses = ShippingAdress.objects.all()
            if addresses and selectDefault == True:
                for addres in addresses:
                    addres.default = False
                    addres.save()
            newAddr = ShippingAdress.objects.create(user_id=request.user.id,
                                                    name=name, surname=surname, phone=phone, country=country, city=city, address=address, situation=exactAddress, default=selectDefault)
            newAddr.save()
            serializer = ShippingAdressSerializer(newAddr)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            return JsonResponse(errors, status=400, safe=False)


def closeOrder(request, id):
    order = {}
    if request.user.is_authenticated:
        order = Order.objects.filter(pk=int(id)).first()
        if order:
            order.complete = True
            order.save()
            items = OrderItem.objects.filter(user_id=request.user.id)
            items.delete()
        else:
            pass
    else:
        order = Order.objects.filter(nberInvoice=str(id)).first()
        order.complete = True
        order.save()
        if 'cartData' in request.session:
            del request.session['cartData']

    context = {
        'order': order
    }
    return render(request, 'emails/confirm.html', context)


@transaction.atomic
def confirmOrder(request):
    data = request.POST
    errors = {}
    tableItems = []
    tabInfoAnonUser = []
    if request.user.is_authenticated and request.is_ajax():
        idAddress = data['idAddress']
        idOrder = data['idOrder']
        payment = checkPayment('payment', data['methodPayment'], errors)

        if idAddress == 'undefined':
            errors['address'] = 'Veuillez entrer une adresse de livraison'
        if len(errors) == 0:
            orderNumber = gererateOrderNber('AfStror', 5)
            invoiceNber = generateNumber('A', 6)

            order = Order.objects.filter(id=int(idOrder)).first()
            if order:
                allItems = order.items.all().order_by('date_added')
                for item in allItems:
                    tableItems.append({
                        'title': item.title,
                        'price': str(item.price),
                        'size': item.size,
                        'color': item.color,
                        'quantity': item.quantity,
                        'total': str(item.total),
                        'path': item.product.mainImg.url,
                        'emailProvider': item.product.user.email,
                        'phoneProvider': item.product.user.phone,
                    })
                order.commandProducts = json.dumps(tableItems)
                order.orderNumber = orderNumber
                order.nberInvoice = invoiceNber
                order.address_id = int(idAddress)
                order.paymentMethod = payment
                # order.newTotal =
                order.save()

            return JsonResponse('success', status=200, safe=False)
        else:
            return JsonResponse(errors, status=400, safe=False)
    else:
        bigTotal = 0
        name = data['name']
        surname = data['surname']
        exactAddress = data['exactAddress']
        phone = checkPhoneError('phone', data['phone'], errors)
        country = checkLenOfField('country', data['country'], 2, errors)
        city = checkLenOfField('city', data['city'], 2, errors)
        address = checkLenOfField('address', data['address'], 2, errors)
        email = setEmailError('email', data['email'], errors)
        payment = checkPayment('payment', data['methodPayment'], errors)
        if len(errors) == 0:
            cart_data = request.session['cartData']
            orderNumber = gererateOrderNber('AfStror', 5)
            invoiceNber = generateNumber('A', 6)
            order = Order.objects.create(
                nberInvoice=invoiceNber, orderNumber=orderNumber)
            order.paymentMethod = payment
            order.save()
            tabInfoAnonUser.append({
                'name': name,
                'surname': surname,
                'exactAddress': exactAddress,
                'phone': phone,
                'country': country,
                'city': city,
                'address': address,
                'email': email,

            })
            for item in cart_data:
                bigTotal += cart_data[item]['subTotal']
                tableItems.append({
                    'title': cart_data[item]['title'],
                    'price': cart_data[item]['price'],
                    'size': cart_data[item]['size'],
                    'color': cart_data[item]['color'],
                    'quantity': cart_data[item]['qte'],
                    'total': cart_data[item]['subTotal'],
                    'path': cart_data[item]['path'],
                    'phoneProvider': cart_data[item]['phoneProvider'],
                    'emailProvider': cart_data[item]['emailProvider']
                })
            order.newTotal = bigTotal
            order.infoAnonUser = json.dumps(tabInfoAnonUser)
            order.commandProducts = json.dumps(tableItems)
            order.save()
            return JsonResponse({'success': 'success', 'id': invoiceNber}, status=200, safe=False)
        else:
            return JsonResponse(errors, status=400, safe=False)
