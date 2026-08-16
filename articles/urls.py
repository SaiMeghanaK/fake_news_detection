from django.urls import path
from .views import (
    ArticleListCreateView,
    ArticleDetailView,
    WriterArticlesView,
    LikeArticleView,
    BookmarkArticleView,
    CategoryListView,
)

urlpatterns = [
    path(
        "",
        ArticleListCreateView.as_view(),
        name="article-list-create"
    ),
    path(
        "<int:pk>/",
        ArticleDetailView.as_view(),
        name="article-detail"
    ),
    path(
        "writer/my-articles/",
        WriterArticlesView.as_view(),
        name="writer-articles"
    ),
    path(
        "<int:pk>/like/",
        LikeArticleView.as_view(),
        name="article-like"
    ),
    path(
        "<int:pk>/bookmark/",
        BookmarkArticleView.as_view(),
        name="article-bookmark"
    ),
    path(
        "categories/",
        CategoryListView.as_view(),
        name="categories"
    ),
]