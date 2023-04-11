import json
from turtle import title
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from registerProduct.models import RegisterProduct
from shop.models import Wishlist
PRODUCTS_PER_PAGE = 2
# Create your views here.


class ListProducts(ListView):
    template_name = 'shop/shop.html'
    model = RegisterProduct
    context_object_name = 'products'
    paginate_by: 1


def listProducts(request):
    ordering = request.GET.get('ordering', '')
    search = request.GET.get('search', '')
    price = request.GET.get('price', '')
    catId = request.GET.get('category_id', '')
    brandId = request.GET.get('brand_id', '')
    productss = RegisterProduct.objects.filter(
        user__statut=True, availability=True, validateProd=True)

    if search:
        products = RegisterProduct.objects.filter(user__statut=True, title__icontains=search, availability=True, validateProd=True) | RegisterProduct.objects.filter(
            user__statut=True, availability=True, validateProd=True, category__name__istartswith=search)
    else:
        products = RegisterProduct.objects.filter(
            user__statut=True, availability=True, validateProd=True)

    if price:
        minPrice = price.split(';')[0]
        maxPrice = price.split(';')[-1]
        products = products.filter(price__range=[minPrice, maxPrice])

    if ordering:
        products = products.order_by(ordering)

    if catId:
        products = products.filter(category_id=catId)

    if brandId:
        products = products.filter(brand_id=brandId)

    page = request.GET.get('page', 1)
    product_paginator = Paginator(products, PRODUCTS_PER_PAGE)
    try:
        products = product_paginator.page(page)
    except EmptyPage:
        products = product_paginator.page(product_paginator.num_pages)
    except:
        products = product_paginator.page(PRODUCTS_PER_PAGE)
    context = {
        'products': products,
        'page_obj': products,
        'is_paginated': True,
        'current_page': page,
        'productss': productss,
        'paginator': product_paginator,
    }
    return render(request, 'shop/shop.html', context)


def suggestionApi(request):
    if 'term' in request.GET:  # term vient de l'API de JQuery
        search = request.GET.get('term')
        qs = RegisterProduct.objects.filter(title__icontains=search)[0:10]
        titles = list()
        for produt in qs:
            titles.append(produt.title)
        if len(qs) < 10:
            length = 10 - len(qs)
            qs2 = RegisterProduct.objects.filter(
                brand__name__icontains=search)[0:length]
            for product in qs2:
                titles.append(product.brand.name)
    return JsonResponse(titles, safe=False)


@login_required(login_url='authentication:loginTempl')
def apiWishlist(request):
    errors = {}
    if request.method == 'POST':
        data = request.POST
        idProd = data['idProd']
        wishCheck = Wishlist.objects.filter(product_id=int(idProd))
        if wishCheck.exists():
            errors['wish'] = 'Cette article existe déja dans la liste de souhait'
        else:
            wishlist = Wishlist.objects.create(
                user_id=request.user.id, product_id=int(idProd))
            wishlist.save()
        if len(errors) == 0:
            return JsonResponse('success', safe=False, status=200)
        else:
            return JsonResponse(errors, safe=False, status=400)


@login_required(login_url='authentication:loginTempl')
def wishlist(request):
    wishlists = Wishlist.objects.all().order_by('-date_added')
    context = {
        'wishlists': wishlists
    }
    return render(request, 'shop/wishlist.html', context)


@login_required(login_url='authentication:loginTempl')
def removeItemWishlist(request):
    idProd = request.POST['idProd']
    lenList = 0
    itemDelete = get_object_or_404(Wishlist, product_id=int(idProd))
    itemDelete.delete()
    wishs = Wishlist.objects.exclude(id=int(idProd))
    if wishs:
        lenList = len(wishs)
    return JsonResponse({'success': 'delete', 'lenList': lenList}, safe=False, status=200)
