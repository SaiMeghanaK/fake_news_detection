from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    Article,
    Category,
    Like,
    Bookmark,
)
from .serializers import (
    ArticleSerializer,
    CategorySerializer,
)
from predictions.ml import predict_fake_news
from predictions.models import Prediction
from notifications.models import Notification

class ArticleListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        articles = Article.objects.filter(
            status="published"
        ).order_by("-published_at")
        serializer = ArticleSerializer(
            articles,
            many=True
        )
        return Response(
            serializer.data
        )

    def post(self, request):
        if request.user.role != "writer":
            return Response(
                {
                    "error":
                    "Only writers can create articles."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ArticleSerializer(
            data=request.data
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        article = serializer.save(
            author=request.user
        )
        label, probability = predict_fake_news(
            article.title,
            article.content
        )
        article.prediction = label
        article.prediction_probability = probability
        if label == "real":
            article.status = "published"
            article.published_at = timezone.now()
        else:
            article.status = "flagged"
            Notification.objects.create(
                recipient=request.user,
                article=article,
                notification_type="flagged",
                message=(
                    f'Your article "{article.title}" '
                    "has been flagged for administrator review."
                )
            )
        article.save()
        Prediction.objects.create(
            article=article,
            prediction=label,
            probability=probability
        )
        return Response(
            ArticleSerializer(article).data,
            status=status.HTTP_201_CREATED
        )

class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            article = Article.objects.get(
                pk=pk
            )
        except Article.DoesNotExist:
            return Response(
                {"error": "Article not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if (
            article.status != "published"
            and
            request.user != article.author
            and
            not request.user.is_superuser
        ):
            return Response(
                {"error": "Article not available."},
                status=status.HTTP_403_FORBIDDEN
            )
        article.views += 1
        article.save(
            update_fields=["views"]
        )
        return Response(
            ArticleSerializer(article).data
        )

class WriterArticlesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.role != "writer":
            return Response(
                {"error": "Writer access required."},
                status=status.HTTP_403_FORBIDDEN
            )
        articles = Article.objects.filter(
            author=request.user
        ).order_by("-created_at")
        return Response(
            ArticleSerializer(
                articles,
                many=True
            ).data
        )

class LikeArticleView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            article = Article.objects.get(
                pk=pk,
                status="published"
            )
        except Article.DoesNotExist:
            return Response(
                {"error": "Article not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        like, created = Like.objects.get_or_create(
            user=request.user,
            article=article
        )
        if not created:
            like.delete()
            return Response({
                "message": "Article unliked."
            })
        return Response({
            "message": "Article liked."
        })

class BookmarkArticleView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            article = Article.objects.get(
                pk=pk,
                status="published"
            )
        except Article.DoesNotExist:
            return Response(
                {"error": "Article not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            article=article
        )
        if not created:
            bookmark.delete()
            return Response({
                "message": "Bookmark removed."
            })
        return Response({
            "message": "Article bookmarked."
        })

class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        categories = Category.objects.all()
        return Response(
            CategorySerializer(
                categories,
                many=True
            ).data
        )