from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by("-created_at")
        return Response(
            NotificationSerializer(
                notifications,
                many=True
            ).data
        )

class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:

            notification = Notification.objects.get(
                pk=pk,
                recipient=request.user
            )
        except Notification.DoesNotExist:
            return Response(
                {"error": "Notification not found."},
                status=404
            )
        notification.is_read = True
        notification.save(
            update_fields=["is_read"]
        )
        return Response({
            "message": "Notification marked as read."
        })