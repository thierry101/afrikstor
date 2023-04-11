from django.urls import path

from blog.api.views import BlogAPIView, BlogEditAPIView


urlpatterns = [
    path('blog/', BlogAPIView.as_view(), name="blogApi"),
    path('edit-blog/<int:pk>/', BlogEditAPIView.as_view(), name="editBlogApi"),
]
app_name = 'blogApi'
