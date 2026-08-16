from django.urls import path
from .web_views import (
    admin_dashboard,
    flagged_articles,
    review_article,
    approve_article,
    reject_article,
)

urlpatterns = [
    path(
        "administrator/dashboard/",
        admin_dashboard,
        name="administrator-dashboard"
    ),
    path(
        "administrator/flagged/",
        flagged_articles,
        name="flagged-articles-page"
    ),
    path(
        "administrator/review/<int:pk>/",
        review_article,
        name="review-article"
    ),
    path(
        "administrator/approve/<int:pk>/",
        approve_article,
        name="approve-article-page"
    ),
    path(
        "administrator/reject/<int:pk>/",
        reject_article,
        name="reject-article-page"
    ),
]