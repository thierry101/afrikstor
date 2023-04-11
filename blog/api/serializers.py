from rest_framework.serializers import ModelSerializer
from authentication.api.serializers import UserSerializer
from blog.models import CommentBlog, modelBlog


class BlogSerializer(ModelSerializer):
    class Meta:
        model = modelBlog

        fields = "__all__"


class CommentBlogSerializer(ModelSerializer):
    user = UserSerializer()
    blog = BlogSerializer()

    class Meta:
        model = CommentBlog

        fields = "__all__"
