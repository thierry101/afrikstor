from django.urls import path, include

from blog.views import commentsBlog, detailBlog, indexBlog, indexFaq


urlpatterns = [
    path('api/', include('blog.api.urls', namespace='mesgHandle')),
    path('list-blog/', indexBlog, name='listBlog'),
    path('detail-blog/<int:id>/', detailBlog, name='detailBlog'),
    path('comment-blog/', commentsBlog, name='commentsBlog'),
    path('faq/', indexFaq, name='indexBlog'),
]
app_name = 'blog'
