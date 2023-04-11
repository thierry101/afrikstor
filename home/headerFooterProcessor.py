from django.http import JsonResponse
from adminProduct.models import Brand, Category
from backend.utils import getTotalPrice
from handleCart.models import Order
from registerProduct.models import RegisterProduct
from settingSite.models import SettingSite
from django.db.models import Count
from django.conf import settings


def linkHeaderFooter(request):
    counterItems = 0
    allItems = []
    idOrder = 0
    bigTotal = 0
    reduction = 0
    newBigTotal = 0
    debug_flag = settings.DEBUG

    try:
        setting = SettingSite.objects.get(state=True)
    except SettingSite.DoesNotExist:
        setting = None
    categories = Category.objects.filter(statut=True).annotate(
        registerProduct_count=Count('registerProduct'))
    brands = Brand.objects.filter(statut=True)
    if request.user.is_authenticated:
        bigTotal = getTotalPrice(Order, request)
        order = Order.objects.filter(
            user_id=request.user.id, complete=False).first()
        if order:
            allItems = order.items.all().order_by('date_added')
            idOrder = order.id
            counterItems = allItems.count()
            if order.reduction:
                reduction = order.reduction
                newBigTotal = order.newTotal
            else:
                newBigTotal = bigTotal

        return {
            'setting': setting,
            'categories': categories,
            'brands': brands,
            'counterItems': counterItems,
            'allItems': allItems,
            'idOrder': idOrder,
            'bigTotal': bigTotal,
            'reduction': reduction,
            'newBigTotal': newBigTotal,
            'debug_flag': debug_flag,
        }
    else:
        if 'cartData' in request.session:
            items = request.session['cartData']
            for item in items:
                ite = RegisterProduct.objects.get(id=int(item))
                allItems.append({'product': ite, 'other': items[item]})
                bigTotal += items[item]['subTotal']

        return {'allItems': allItems,
                'bigTotal': bigTotal,
                'setting': setting,
                'categories': categories,
                'brands': brands,
                'debug_flag': debug_flag,

                }
