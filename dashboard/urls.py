from django.urls import path
from .views import (
    AdminDashboardView,
    FlaggedArticlesView,
    ApproveArticleView,
    RejectArticleView,
)

urlpatterns = [
    path(
        "",
        AdminDashboardView.as_view(),
        name="admin-dashboard"
    ),
    path(
        "flagged/",
        FlaggedArticlesView.as_view(),
        name="flagged-articles"
    ),
    path(
        "approve/<int:pk>/",
        ApproveArticleView.as_view(),
        name="approve-article"
    ),
    path(
        "reject/<int:pk>/",
        RejectArticleView.as_view(),
        name="reject-article"
    ),
]