import base64
import json
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from django.core.files.base import ContentFile
from adminProduct.models import Size
from django.shortcuts import get_object_or_404

from authentication.authentication import JWTAuthentication
from authentication.permissions import IsOwnerOrReadOnly, ProvidersPermissions, ValidatorsPermissions
from backend.regex import checkExtensionImg, checkExtensionUpdateColorImg, checkExtensionImgUpdate, checkExtensionOfColorImg, checkExtensionOfManyImg, checkExtensionUpdateManyImg, checkLenOfField, checkPrices, checkSoldPrice, checkStatus, checkTableColor, checkTableId, convertToInt, deleteOneImg, deletePathManyImg, id_generator
from backend.utils import sendMessage
from registerProduct.api.serializers import RegisterProductSerializer
from registerProduct.models import RegisterProduct
from settingSite.models import SettingSite


class GetAllProductsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = RegisterProductSerializer
    permission_classes = [IsAuthenticated & ValidatorsPermissions]

    def get(self, request):
        allProducts = RegisterProduct.objects.all()
        serializer = RegisterProductSerializer(allProducts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ******************* to reject or confirm show product ************************
class GetAllProductsEditAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = RegisterProductSerializer
    permission_classes = [IsAuthenticated & ValidatorsPermissions]

    def get_object(self, pk):
        product = get_object_or_404(RegisterProduct, pk=int(pk))
        return product

    @transaction.atomic
    def put(self, request, pk):
        product = self.get_object(pk)
        errors = {}
        if request.method == 'PUT':
            data = request.data
            user = data['user']
            email = user['email']
            article = data['article']
            validProduct = data['productValid']
            message = checkLenOfField('message', data['text'], 5, errors)
            if validProduct == False and len(errors) == 0:
                product.rejectReason = message
                product.validateProd = False
                product.save()
                logo = SettingSite.objects.get(state=True).logo
                path = f"{ request.scheme }://{ request.META.get('HTTP_HOST') }"
                sendMessage(f"Raison du rejet de l'article {article}", 'emails/rejetMail.html',
                            {'user': user,
                             'article': article,
                             'logo': logo,
                             'path': path,
                             'message': message}, settings.EMAIL_HOST_USER, (email,))
                return Response('false', status=status.HTTP_200_OK)
            elif validProduct == True:
                product.validateProd = True
                product.save()
                serializer = RegisterProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterProductAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = RegisterProductSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]

    def get(self, request):
        allProducts = RegisterProduct.objects.filter(
            user_id=request.user.id).order_by('-updated')
        rejetsProducts = RegisterProduct.objects.filter(
            user_id=request.user.id, validateProd=False).order_by('-updated')
        serializerValid = RegisterProductSerializer(allProducts, many=True)
        serializerReject = RegisterProductSerializer(rejetsProducts, many=True)
        return Response({'validsProd': serializerValid.data, 'rejectsProd': serializerReject.data}, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        data = request.data
        errors = {}
        tabOtherIMgs = []
        tabColorIMgs = []
        cat_id = convertToInt(
            'cat_id', data['category_id'], 'une catégorie', errors)
        sub_cat_id = convertToInt(
            'sub_cat', data['sub_category_id'], 'une sous-catégorie', errors)
        brand_id = convertToInt(
            'brand_id', data['brand_id'], 'une marque', errors)
        name = checkLenOfField('name', data['name'], 2, errors)
        price = checkPrices('price', data['price'], errors)
        sold_price = checkSoldPrice(
            'sold_price', price, data['sold_price'], errors)
        # *************************
        nameMainImg = checkExtensionImg(
            'mainImg', data['mainIMg'], 'name', 'file', errors)
        nameSecondImg = checkExtensionImg(
            'secondIMg', data['secondIMg'], 'name', 'file', errors)
        tableOtherImgs = checkExtensionOfManyImg(
            'other_img', data['tableOtherImg'], errors)
        tableColorImgs = checkExtensionOfColorImg(
            'colorImgs', data['tableColorImg'], errors)
        tableColors = data['colors']
        tableSizes = data['sizes']
        description = checkLenOfField(
            'description', data['description'], 5, errors)
        available = data['available']
        if len(errors) == 0:
            slug = id_generator()
            product = RegisterProduct.objects.create(user_id=request.user.id, category_id=cat_id, subCategory_id=sub_cat_id, brand_id=brand_id,
                                                     title=name, price=price, sold_price=sold_price, colors=json.dumps(tableColors), description=description, availability=available)
            product.save()
            # save sizes
            for siz in tableSizes:
                product.sizes.add(Size.objects.get(pk=int(siz['id'])))
            product.save()

            # save main img
            format, imgstr = data['mainIMg']['file'].split(';base64,')
            # You can save this as file instance.
            product.mainImg = ContentFile(base64.b64decode(imgstr),
                                          name=str(slug)+str(nameMainImg))
            product.save()

            # save second main img
            format, imgstr = data['secondIMg']['file'].split(';base64,')
            # You can save this as file instance.
            product.secondImg = ContentFile(base64.b64decode(imgstr),
                                            name=str(slug)+str(nameSecondImg))
            product.save()

            # save other imgs
            for img in data['tableOtherImg']:
                unique = id_generator()
                format, imgstr = img['file'].split(';base64,')
                ext = format.split('/')[-1]
                product.othersImgs = ContentFile(
                    base64.b64decode(imgstr), name=str(unique) + '.' + ext)
                product.save()
                tabOtherIMgs.append({'file': product.othersImgs.url})
            product.tabOtherImgs = json.dumps(tabOtherIMgs)
            product.save()

            # save colors images
            for img in data['tableColorImg']:
                nameImg = id_generator()
                format, imgstr = img['img'].split(';base64,')
                ext = format.split('/')[-1]
                product.colorsImgs = ContentFile(
                    base64.b64decode(imgstr), name=str(nameImg) + '.' + ext)
                product.save()
                tabColorIMgs.append(
                    {'name': img['color'], 'hex': img['hex'], 'img': product.colorsImgs.url})
            product.colorimgs = json.dumps(tabColorIMgs)
            product.save()
            serializer = RegisterProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterProductDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = RegisterProductSerializer
    permission_classes = [IsAuthenticated &
                          IsOwnerOrReadOnly]

    def get_object(self, pk):
        product = get_object_or_404(RegisterProduct, pk=int(pk))
        return product

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = RegisterProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, pk):
        product = self.get_object(pk)
        newTableOthersImg = []
        tablebase64 = []
        tablebase64Color = []
        newTableColorsImg = []
        errors = {}
        if request.method == 'PUT':
            data = request.data
            if 'statut' in data:
                statut = checkStatus(data['value'])
                product.availability = statut
                product.save()
                return Response('success', status=status.HTTP_200_OK)
            else:
                oldTabOtherImgs = json.loads(product.tabOtherImgs)
                tableFromUser = list(data['tableOtherImg'])
                if product.colorimgs:
                    oldTabColorImgs = json.loads(product.colorimgs)
                else:
                    oldTabColorImgs = []
                tableCOlorFromUer = list(data['tableColorImg'])
                cat_id = convertToInt(
                    'cat_id', data['category_id'], 'une catégorie', errors)
                sub_cat_id = convertToInt(
                    'sub_cat', data['sub_category_id'], 'une sous-catégorie', errors)
                brand_id = convertToInt(
                    'brand_id', data['brand_id'], 'une marque', errors)
                name = checkLenOfField('name', data['name'], 2, errors)
                price = checkPrices('price', data['price'], errors)
                available = checkStatus(data['available'])
                tableColors = data['colors']
                tableSizes = data['sizes']
                description = checkLenOfField(
                    'description', data['description'], 5, errors)
                sold_price = checkSoldPrice(
                    'sold_price', price, data['sold_price'], errors)
                if data['mainIMg']['name'] != '':
                    nameMainImg = checkExtensionImgUpdate(
                        'mainImg', data['mainIMg'], 'name', 'file', product.mainImg, errors)
                else:
                    pass
                if data['secondIMg']['name'] != '':
                    nameSecondImg = checkExtensionImgUpdate(
                        'secondIMg', data['secondIMg'], 'name', 'file', product.secondImg, errors)
                else:
                    pass
                tableOtherImgs = checkExtensionUpdateManyImg(
                    'other_img', 'file', oldTabOtherImgs, tableFromUser, tablebase64, newTableOthersImg, errors)
                tableColorImgs = checkExtensionUpdateColorImg(
                    'colorImgs', 'img', 'name', 'hex', oldTabColorImgs, tableCOlorFromUer, tablebase64Color, newTableColorsImg, errors)
                if len(errors) == 0:
                    slug = id_generator()
                    # product.user_id = request.user.id
                    product.category_id = cat_id
                    product.subCategory_id = sub_cat_id
                    product.brand_id = brand_id
                    product.title = name
                    product.price = price
                    product.sold_price = sold_price
                    product.description = description
                    product.availability = available
                    product.colors = json.dumps(tableColors)
                    product.save()
                    # save sizes
                    for siz in tableSizes:
                        product.sizes.add(Size.objects.get(pk=int(siz['id'])))
                        product.save()

                    # save mainImg
                    if data['mainIMg']['name'] != '':
                        format, imgstr = data['mainIMg']['file'].split(
                            ';base64,')
                        # You can save this as file instance.
                        dataImg = ContentFile(base64.b64decode(imgstr),
                                              name=str(slug)+str(nameMainImg))
                        product.mainImg = dataImg
                        product.save()
                    else:
                        pass

                     # save second mainImg
                    if data['secondIMg']['name'] != '':
                        format, imgstr = data['secondIMg']['file'].split(
                            ';base64,')
                        # You can save this as file instance.
                        dataImg = ContentFile(base64.b64decode(imgstr),
                                              name=str(slug)+str(nameSecondImg))
                        product.secondImg = dataImg
                        product.save()
                    else:
                        pass

                    # save other image
                    if len(tablebase64) > 0:
                        for img in tableOtherImgs['base64']:
                            unique = id_generator()
                            format, imgstr = img.split(';base64,')
                            ext = format.split('/')[-1]
                            product.othersImgs = ContentFile(
                                base64.b64decode(imgstr), name=str(unique) + '.' + ext)
                            product.save()
                            newTableOthersImg.append(
                                {'file': product.othersImgs.url})
                        product.tabOtherImgs = json.dumps(newTableOthersImg)
                        product.save()

                    # save color img
                    if len(tablebase64Color) > 0:
                        for img in tableColorImgs['base64']:
                            unique = id_generator()
                            format, imgstr = img['img'].split(';base64,')
                            ext = format.split('/')[-1]
                            product.colorsImgs = ContentFile(
                                base64.b64decode(imgstr), name=str(unique) + '.' + ext)
                            product.save()
                            newTableColorsImg.append(
                                {'name': img['color'], 'hex': img['hex'], 'img': product.colorsImgs.url})
                        product.colorimgs = json.dumps(newTableColorsImg)
                        product.save()
                    serializer = RegisterProductSerializer(product)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)

        deleteOneImg(product.mainImg)
        deleteOneImg(product.secondImg)
        deletePathManyImg(product.tabOtherImgs, 'file')
        deletePathManyImg(product.colorimgs, 'img')
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
