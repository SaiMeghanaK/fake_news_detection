from rest_framework import serializers
from .models import (
    Article,
    Category,
    Like,
    Bookmark,
)

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source="author.email",
        read_only=True
    )
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "author",
            "author_name",
            "title",
            "content",
            "category",
            "image",
            "prediction",
            "prediction_probability",
            "status",
            "admin_comment",
            "created_at",
            "updated_at",
            "published_at",
            "views",
            "likes_count",
        ]
        read_only_fields = [
            "author",
            "prediction",
            "prediction_probability",
            "status",
            "admin_comment",
            "published_at",
            "views",
        ]

    def get_likes_count(self, obj):

        return obj.likes.count()

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = [
            "id",
            "user",
            "article",
            "created_at",
        ]
        read_only_fields = [
            "user"
        ]

class BookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = [
            "id",
            "user",
            "article",
            "created_at",
        ]
        read_only_fields = [
            "user"
        ]