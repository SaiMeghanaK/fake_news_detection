from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Article,
    Category,
    Like,
    Bookmark,
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "author",
        "prediction",
        "status",
        "created_at",
    ]
    list_filter = [
        "status",
        "prediction",
        "category",
    ]
    search_fields = [
        "title",
        "content",
        "author__email",
    ]

admin.site.register(Like)
admin.site.register(Bookmark)