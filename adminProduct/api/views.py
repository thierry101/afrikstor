import base64
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from adminProduct.api.serializers import *
from rest_framework import status
from authentication.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.files.base import ContentFile
from django.db import transaction
from django.shortcuts import get_object_or_404

from adminProduct.models import *
from authentication.permissions import AdminPermissions
from backend.regex import checkExtensionImg, checkExtensionImgUpdate, checkIdSelected, checkLenOfField, checkStatus, checkUniqueItem, checkUpdateField, id_generator


class CategoryAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    # Cache page for the requested url

    def get(self, request):
        categories = Category.objects.all().order_by('-updated')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        data = request.data
        errors = {}
        title = checkLenOfField('title', data['title'], 2, errors)
        # description = checkLenOfField(
        #     'description', data['description'], 2, errors)
        # nameMainImg = checkExtensionImg(
        #     'logo', data['logo'], 'name', 'file', errors)
        statut = checkStatus(data['statut'])
        title = checkUniqueItem('title', Category, title, errors)

        if len(errors) == 0:
            slug = id_generator()
            category = Category.objects.create(
                name=title, statut=statut)
            category.save()
            # format, imgstr = data['logo']['file'].split(';base64,')
            # You can save this as file instance.
            # data = ContentFile(base64.b64decode(imgstr),
            #                    name=str(slug)+str(nameMainImg))
            # category.image = data
            category.save()
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get_object(self, pk):
        category = get_object_or_404(Category, pk=int(pk))
        return category

    # Cache page for the requested url

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        # rgerye
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, pk):
        category = self.get_object(pk)
        errors = {}
        if request.method == 'PUT':
            data = request.data
            if 'changeState' in data:
                statut = checkStatus(data['newState'])
                category.statut = statut
                category.save()
                return Response('success', status=status.HTTP_200_OK)
            else:
                title = checkLenOfField('title', data['title'], 2, errors)
                # description = checkLenOfField(
                #     'description', data['description'], 2, errors)
                # nameMainImg = checkExtensionImgUpdate(
                #     'logo', data['logo'], 'name', 'file', category.image, errors)
                statut = checkStatus(data['statut'])
                # title = checkUniqueItem('title', Category, title, errors)

                if len(errors) == 0:
                    slug = id_generator()
                    category.name = title
                    # category.description = description
                    category.statut = statut
                    category.save()
                    if data['logo']['name'] != '':
                        format, imgstr = data['logo']['file'].split(';base64,')
                        # You can save this as file instance.
                        # data = ContentFile(base64.b64decode(imgstr),
                        #                    name=str(slug)+str(nameMainImg))
                        # category.image = data
                        category.save()
                    serializer = CategorySerializer(category)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        # mainImg = "/" + str(category.image)
        # if(mainImg == '/'):
        #     category.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        # else:
        #     if os.path.exists(settings.MEDIA_ROOT + mainImg):
        #         os.remove(settings.MEDIA_ROOT + mainImg)
        #     else:
        #         pass
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubCategoryAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]

    # Cache page for the requested url

    def get(self, request):
        subCategories = SubCategory.objects.all().order_by('-updated')
        serializer = SubCategorySerializer(subCategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        data = request.data
        errors = {}
        id_cat = checkIdSelected(
            'category_id', data['category_id'], 'une catégorie', errors)
        title = checkLenOfField('title', data['title'], 2, errors)
        # description = checkLenOfField(
        #     'description', data['description'], 2, errors)
        # nameMainImg = checkExtensionImg(
        #     'logo', data['logo'], 'name', 'file', errors)
        statut = checkStatus(data['statut'])
        title = checkUniqueItem('title', SubCategory, title, errors)

        if len(errors) == 0:
            slug = id_generator()
            subcategory = SubCategory.objects.create(category_id=id_cat,
                                                     name=title, statut=statut)
            subcategory.save()
            # format, imgstr = data['logo']['file'].split(';base64,')
            # # You can save this as file instance.
            # data = ContentFile(base64.b64decode(imgstr),
            #                    name=str(slug)+str(nameMainImg))
            # subcategory.image = data
            subcategory.save()
            serializer = SubCategorySerializer(subcategory)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategoryDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get_object(self, pk):
        subCategory = get_object_or_404(SubCategory, pk=int(pk))
        return subCategory

    # Cache page for the requested url

    def get(self, request, pk):
        subCategory = self.get_object(pk)
        serializer = CategorySerializer(subCategory)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, pk):
        subCategory = self.get_object(pk)
        errors = {}
        if request.method == 'PUT':
            data = request.data
            if 'changeState' in data:
                statut = checkStatus(data['newState'])
                subCategory.statut = statut
                subCategory.save()
                return Response('success', status=status.HTTP_200_OK)
            else:
                id_cat = checkIdSelected(
                    'category_id', data['category_id'], 'une catégorie', errors)
                title = checkLenOfField('title', data['title'], 2, errors)
                # description = checkLenOfField(
                #     'description', data['description'], 2, errors)
                # nameMainImg = checkExtensionImgUpdate(
                #     'logo', data['logo'], 'name', 'file', subCategory.image, errors)
                statut = data['statut']
                # title = checkUniqueItem('title', SubCategory, title, errors)

                if len(errors) == 0:
                    slug = id_generator()
                    subCategory.category_id = id_cat
                    subCategory.name = title
                    # subCategory.description = description
                    subCategory.statut = statut
                    subCategory.save()
                    # if data['logo'] and data['logo']['name'] != '':
                    #     format, imgstr = data['logo']['file'].split(';base64,')
                    #     # You can save this as file instance.
                    #     data = ContentFile(base64.b64decode(imgstr),
                    #                        name=str(slug)+str(nameMainImg))
                    #     subCategory.image = data
                    #     subCategory.save()
                    serializer = SubCategorySerializer(subCategory)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subCategory = self.get_object(pk)
        mainImg = "/" + str(subCategory.image)
        # if(mainImg == '/'):
        #     subCategory.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        # else:
        #     if os.path.exists(settings.MEDIA_ROOT + mainImg):
        #         os.remove(settings.MEDIA_ROOT + mainImg)
        #     else:
        #         pass
        subCategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SizeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated]

    # Cache page for the requested url

    def get(self, request):
        sizes = Size.objects.all().order_by('-updated')
        serializer = SizeSerializer(sizes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        data = request.data
        errors = {}
        title = checkLenOfField('name', data['name'], 1, errors)
        statut = checkStatus(data['statut'])
        title = checkUniqueItem('name', Size, title, errors)

        if len(errors) == 0:
            size = Size.objects.create(name=title, statut=statut)
            size.save()
            serializer = SizeSerializer(size)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SizeDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get_object(self, pk):
        size = get_object_or_404(Size, pk=int(pk))
        return size

    # Cache page for the requested url

    def get(self, request, pk):
        size = self.get_object(pk)
        serializer = SizeSerializer(size)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, pk):
        size = self.get_object(pk)
        errors = {}
        if request.method == 'PUT':
            data = request.data
            if 'changeState' in data:
                statut = checkStatus(data['newState'])
                size.statut = statut
                size.save()
                return Response('success', status=status.HTTP_200_OK)
            else:
                title = checkLenOfField('name', data['name'], 1, errors)
                statut = checkStatus(data['statut'])
                title = checkUniqueItem('name', Size, title, errors)

                if len(errors) == 0:
                    size.name = title
                    size.statut = statut
                    size.save()
                    serializer = SizeSerializer(size)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        size = self.get_object(pk)
        size.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BrandAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]

    # Cache page for the requested url

    def get(self, request):
        brands = Brand.objects.all().order_by('-updated')
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        data = request.data
        errors = {}
        title = checkLenOfField('title', data['title'], 1, errors)
        description = checkUpdateField(data['description'])
        statut = checkStatus(data['statut'])
        nameMainImg = checkExtensionImg(
            'logo', data['logo'], 'name', 'file', errors)

        if len(errors) == 0:
            slug = id_generator()
            brand = Brand.objects.create(
                name=title, description=description, statut=statut)
            brand.save()
            format, imgstr = data['logo']['file'].split(';base64,')
            # You can save this as file instance.
            data = ContentFile(base64.b64decode(imgstr),
                               name=str(slug)+str(nameMainImg))
            brand.image = data
            print("the data image to save is ", data)
            # brand = Brand.objects.get_or_create(image=data)
            brand.save()
            serializer = BrandSerializer(brand)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class BrandDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated & AdminPermissions]

    def get_object(self, pk):
        brand = get_object_or_404(Brand, pk=int(pk))
        return brand

    # Cache page for the requested url

    def get(self, request, pk):
        brand = self.get_object(pk)
        serializer = BrandSerializer(brand)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, pk):
        brand = self.get_object(pk)
        errors = {}
        if request.method == 'PUT':
            data = request.data
            if 'stateBrand' in data:
                statut = checkStatus(data['stateBrand'])
                brand.statut = statut
                brand.save()
                return Response('success', status=status.HTTP_200_OK)
            else:
                title = checkLenOfField('title', data['title'], 1, errors)
                description = checkUpdateField(data['description'])
                statut = checkStatus(data['statut'])
                nameMainImg = checkExtensionImgUpdate(
                    'logo', data['logo'], 'name', 'file', brand.image, errors)

                if len(errors) == 0:
                    slug = id_generator()
                    brand.name = title
                    brand.description = description
                    brand.statut = statut
                    brand.save()
                    if data['logo']['name'] != '':
                        format, imgstr = data['logo']['file'].split(';base64,')
                        # You can save this as file instance.
                        data = ContentFile(base64.b64decode(imgstr),
                                           name=str(slug)+str(nameMainImg))
                        brand.image = data
                        brand.save()
                    serializer = BrandSerializer(brand)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        brand = self.get_object(pk)
        mainImg = "/" + str(brand.image)
        if(mainImg == '/'):
            brand.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            if os.path.exists(settings.MEDIA_ROOT + mainImg):
                os.remove(settings.MEDIA_ROOT + mainImg)
            else:
                pass
            brand.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        pass
