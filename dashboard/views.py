from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdministrator
from articles.models import Article
from articles.serializers import ArticleSerializer
from notifications.models import Notification

class AdminDashboardView(APIView):
    permission_classes = [IsAdministrator]
    def get(self, request):
        return Response({
            "total_articles":
                Article.objects.count(),
            "published_articles":
                Article.objects.filter(
                    status="published"
                ).count(),
            "flagged_articles":
                Article.objects.filter(
                    status="flagged"
                ).count(),
            "rejected_articles":
                Article.objects.filter(
                    status="rejected"
                ).count(),
            "pending_articles":
                Article.objects.filter(
                    status="pending"
                ).count(),
        })

class FlaggedArticlesView(APIView):
    permission_classes = [IsAdministrator]
    def get(self, request):
        articles = Article.objects.filter(
            status="flagged"
        ).order_by("-created_at")
        return Response(
            ArticleSerializer(
                articles,
                many=True
            ).data
        )

class ApproveArticleView(APIView):
    permission_classes = [IsAdministrator]
    def post(self, request, pk):
        try:
            article = Article.objects.get(
                pk=pk,
                status="flagged"
            )
        except Article.DoesNotExist:
            return Response(
                {"error": "Flagged article not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        article.status = "published"
        article.published_at = timezone.now()
        article.admin_comment = request.data.get(
            "comment",
            "Article approved by administrator."
        )
        article.save()
        Notification.objects.create(
            recipient=article.author,
            article=article,
            notification_type="approved",
            message=(
                f'Your article "{article.title}" '
                "has been approved and published."
            )
        )
        return Response({
            "message": "Article approved and published."
        })

class RejectArticleView(APIView):
    permission_classes = [IsAdministrator]
    def post(self, request, pk):
        try:
            article = Article.objects.get(
                pk=pk,
                status="flagged"
            )
        except Article.DoesNotExist:
            return Response(
                {"error": "Flagged article not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        comment = request.data.get(
            "comment",
            "Article rejected by administrator."
        )
        article.status = "rejected"
        article.admin_comment = comment
        article.save()
        Notification.objects.create(
            recipient=article.author,
            article=article,
            notification_type="rejected",
            message=(
                f'Your article "{article.title}" '
                f"has been rejected. Reason: {comment}"
            )
        )
        return Response({
            "message": "Article rejected."
        })