import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render

from adminProduct.models import Brand
from advert.models import Advert
from backend.regex import checkLenOfField
from blog.models import modelBlog
from contactAndAbout.models import AboutUs
from home.models import CommentProduct
from registerProduct.models import RegisterProduct


# Create your views here.


def indexHome(request):
    aboutUs = AboutUs.objects.filter(available=True).first()
    newProducts = []
    oldProducts = []
    current_date = datetime.datetime.now().date()
    brands = Brand.objects.filter(statut=True)
    products = RegisterProduct.objects.filter(user__statut=True,
                                              availability=True, validateProd=True)[:16]
    adverts = Advert.objects.filter(statut=True)
    blogs = modelBlog.objects.filter(statut=True)
    comments = CommentProduct.objects.all().order_by('-timestamp')

    for prod in products:
        if (prod.updated).date() + datetime.timedelta(days=30) > current_date:
            newProducts.append(prod)
        else:
            oldProducts.append(prod)
    path = f"{ request.scheme }://{ request.META.get('HTTP_HOST') }/media/"
    context = {
        'brands': brands,
        'products': products,
        'url': path,
        'newProducts': newProducts,
        'adverts': adverts,
        'blogs': blogs,
        'comments': comments,
        'aboutUs': aboutUs,
    }
    return render(request, 'home/index.html', context)


def detailProduct(request, id):
    product = RegisterProduct.objects.get(pk=int(id))
    comments = CommentProduct.objects.filter(
        product_id=int(id)).order_by('-timestamp')
    # change M to B to have month in total letter
    related_products = RegisterProduct.objects.exclude(
        category_id=int(product.category_id)).order_by('-updated')  # here the request must exclude the current product
    othersImgs = json.loads(product.tabOtherImgs)
    colors = json.loads(product.colors)
    sizes = product.sizes.all()
    url = f"{ request.scheme }://{ request.META.get('HTTP_HOST') }"
    path = f"{ request.scheme }://{ request.META.get('HTTP_HOST') }/media/"
    context = {
        'product': product,
        'url': url,
        'path': path,
        'othersImgs': othersImgs,
        'colors': colors,
        'sizes': sizes,
        'comments': comments,
        'related_products': related_products,
    }
    return render(request, 'home/single.html', context)


def showProductSByBrands(request, brand, id):
    brand = brand
    path = f"{ request.scheme }://{ request.META.get('HTTP_HOST') }/media/"
    products = RegisterProduct.objects.filter(user__statut=True,
                                              brand_id=int(id), availability=True, validateProd=True)
    allProducts = RegisterProduct.objects.filter(user__statut=True,
                                                 availability=True, validateProd=True)
    context = {
        'products': products,
        'brand': brand,
        'allProducts': allProducts,
        'url': path,
    }
    return render(request, 'home/brand.html', context)


def commentsProduct(request):
    errors = {}
    if request.user.is_authenticated and request.method == 'POST':
        data = request.POST
        idProd = data['idProd']
        comment = checkLenOfField('comment', data['comentProd'], 5, errors)
        if len(errors) == 0:
            comment = CommentProduct.objects.create(
                user_id=request.user.id, product_id=idProd, message=comment)
            comment.save()
            return JsonResponse('success', safe=False, status=200)
        else:
            return JsonResponse(errors, status=400, safe=False)
