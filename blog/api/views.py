import base64
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from django.core.files.base import ContentFile

from authentication.authentication import JWTAuthentication
from authentication.permissions import IsOwnerOrReadOnly, ValidatorsPermissions
from backend.regex import checkExtensionImg, checkExtensionImgUpdate, checkLenOfField
from blog.api.serializers import BlogSerializer
from blog.models import modelBlog


class BlogAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]

    def get(self, request):
        allBlogs = modelBlog.objects.all().order_by('-updated')
        serializer = BlogSerializer(allBlogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        if request.method == 'POST':
            errors = {}
            data = request.data
            title = checkLenOfField('title', data['title'], 2, errors)
            author = checkLenOfField('author', data['author'], 2, errors)
            category = checkLenOfField('category', data['category'], 2, errors)
            article = checkLenOfField('article', data['article'], 2, errors)
            statut = data['statut']
            nameMainImg = checkExtensionImg(
                'mainImg', data['mainIMg'], 'name', 'file', errors)
            if len(errors) == 0:
                blog = modelBlog.objects.create(
                    title=title, category=category, author=author, blogMsg=article, statut=statut)
                blog.save()
                # save main img
                format, imgstr = data['mainIMg']['file'].split(';base64,')
                # You can save this as file instance.
                blog.image = ContentFile(base64.b64decode(imgstr),
                                         name=str(nameMainImg))
                blog.save()
                serializer = BlogSerializer(blog)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class BlogEditAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated & ValidatorsPermissions]

    def get_object(self, pk):
        blog = get_object_or_404(modelBlog, pk=int(pk))
        return blog

    @transaction.atomic
    def put(self, request, pk):
        blog = self.get_object(pk)
        errors = {}
        if request.method == 'PUT':
            datas = request.data
            if not datas['state']:
                newData = datas['data']
                title = checkLenOfField('title', newData['title'], 2, errors)
                author = checkLenOfField(
                    'author', newData['author'], 2, errors)
                category = checkLenOfField(
                    'category', newData['category'], 2, errors)
                article = checkLenOfField(
                    'article', newData['article'], 2, errors)
                statut = newData['statut']
                if newData['mainIMg'] != None and newData['mainIMg']['name'] != '':
                    nameMainImg = checkExtensionImgUpdate(
                        'mainImg', newData['mainIMg'], 'name', 'file', blog.image, errors)
                else:
                    pass
                if len(errors) == 0:
                    blog.title = title
                    blog.category = category
                    blog.author = author
                    blog.blogMsg = article
                    blog.statut = statut
                    blog.save()
                    # save mainImg
                    if newData['mainIMg'] != None and newData['mainIMg']['name'] != '':
                        format, imgstr = newData['mainIMg']['file'].split(
                            ';base64,')
                        # You can save this as file instance.
                        dataImg = ContentFile(base64.b64decode(imgstr),
                                              name=str(nameMainImg))
                        blog.image = dataImg
                        blog.save()
                    else:
                        pass
                    serializer = BlogSerializer(blog)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                newTat = datas['data']
                blog.statut = newTat
                blog.save()
                return Response('success', status=status.HTTP_200_OK)
