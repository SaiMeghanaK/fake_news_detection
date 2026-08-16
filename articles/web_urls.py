from django.urls import path
from .web_views import (
    home_page,
    writer_dashboard,
    create_article,
    article_detail_page,
    like_article,
    bookmark_article,
)

urlpatterns = [
    path(
        "",
        home_page,
        name="home"
    ),
    path(
        "writer/dashboard/",
        writer_dashboard,
        name="writer-dashboard"
    ),
    path(
        "writer/create/",
        create_article,
        name="create-article"
    ),
    path(
        "article/<int:pk>/",
        article_detail_page,
        name="article-detail-page"
    ),
    path(
        "article/<int:pk>/like/",
        like_article,
        name="like-article"
    ),
    path(
        "article/<int:pk>/bookmark/",
        bookmark_article,
        name="bookmark-article"
    ),
]