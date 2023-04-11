from django.http import JsonResponse
from django.shortcuts import render
from backend.regex import checkLenOfField
from django.db import transaction
from blog.api.serializers import CommentBlogSerializer

from blog.models import FAQ, CommentBlog, modelBlog

# Create your views here.


def indexBlog(request):
    blogs = modelBlog.objects.filter(statut=True)
    blogRecents = modelBlog.objects.filter(
        statut=True).order_by('-updated')[:4]
    context = {
        'blogs': blogs,
        'blogRecents': blogRecents,
    }

    return render(request, 'blog/index.html', context)


def detailBlog(request, id):
    blog = modelBlog.objects.get(pk=int(id))
    comments = CommentBlog.objects.filter(blog_id=int(id))
    blogs = modelBlog.objects.filter(statut=True)[:5]
    context = {
        'blog': blog,
        'blogs': blogs,
        'blogDetail': True,
        'comments': comments,
        'countCment': len(comments),
    }
    return render(request, 'blog/blogDetail.html', context)


@transaction.atomic
def commentsBlog(request):
    errors = {}
    if request.is_ajax():
        data = request.POST
        subject = checkLenOfField('subject', data['subject'], 2, errors)
        message = checkLenOfField('message', data['message'], 5, errors)
        idBlog = data['idBlog']
        comments = CommentBlog.objects.filter(blog_id=int(idBlog))
        if len(errors) == 0:
            messag = CommentBlog.objects.create(
                user_id=int(request.user.id), blog_id=int(idBlog), subject=subject, message=message)
            messag.save()
            serializer = CommentBlogSerializer(messag)
            return JsonResponse({'nberBlogs': len(comments), 'data': serializer.data}, status=200, safe=False)
        else:
            return JsonResponse(errors, status=400, safe=False)


def indexFaq(request):
    faqs = FAQ.objects.filter(availability=True)
    context = {
        'faqs': faqs
    }

    return render(request, 'blog/faq.html', context)
