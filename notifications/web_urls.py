from django.urls import path
from .web_views import (
    notifications_page,
    mark_notification_read,
)

urlpatterns = [
    path(
        "notifications/",
        notifications_page,
        name="notifications-page"
    ),
    path(
        "notifications/<int:pk>/read/",
        mark_notification_read,
        name="mark-notification-read"
    ),
]