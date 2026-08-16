from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Notification

@login_required
def notifications_page(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by("-created_at")
    return render(
        request,
        "notifications/notifications.html",
        {
            "notifications": notifications
        }
    )

@login_required
def mark_notification_read(request, pk):
    notification = Notification.objects.filter(
        id=pk,
        recipient=request.user
    ).first()
    if notification:
        notification.is_read = True
        notification.save(
            update_fields=["is_read"]
        )
    return redirect("/notifications/")