from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Article, Category, Like, Bookmark
from predictions.ml import predict_fake_news
from predictions.models import Prediction
from notifications.models import Notification

def home_page(request):
    articles = Article.objects.filter(
        status="published"
    ).select_related(
        "author",
        "category"
    ).order_by("-published_at")
    search = request.GET.get("search")
    if search:
        articles = articles.filter(
            title__icontains=search
        )
    category = request.GET.get("category")
    if category:
        articles = articles.filter(
            category_id=category
        )
    categories = Category.objects.all()
    return render(
        request,
        "home.html",
        {
            "articles": articles,
            "categories": categories,
            "search": search,
        }
    )

@login_required
def writer_dashboard(request):
    if request.user.role != "writer":
        return redirect("/")
    articles = Article.objects.filter(
        author=request.user
    ).order_by("-created_at")
    total_articles = articles.count()
    published_articles = articles.filter(
        status="published"
    ).count()
    flagged_articles = articles.filter(
        status="flagged"
    ).count()
    return render(
        request,
        "articles/writer_dashboard.html",
        {
            "articles": articles,
            "total_articles": total_articles,
            "published_articles": published_articles,
            "flagged_articles": flagged_articles,
        }
    )

@login_required
def create_article(request):
    if request.user.role != "writer":
        return redirect("/")
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")
        image = request.FILES.get("image")
        if not title or not content:
            messages.error(
                request,
                "Title and content are required."
            )
            return render(
                request,
                "articles/create_article.html",
                {"categories": categories}
            )
        category = None
        if category_id:
            category = get_object_or_404(
                Category,
                id=category_id
            )
        article = Article.objects.create(
            author=request.user,
            title=title,
            content=content,
            category=category,
            image=image
        )
        prediction, probability = predict_fake_news(
            title,
            content
        )
        article.prediction = prediction
        article.prediction_probability = probability
        if prediction == "real":
            article.status = "published"
            article.published_at = timezone.now()
            article.save()
            Prediction.objects.create(
                article=article,
                prediction=prediction,
                probability=probability
            )
            messages.success(
                request,
                "Article verified as REAL and published successfully."
            )
        else:
            article.status = "flagged"
            article.save()
            Prediction.objects.create(
                article=article,
                prediction=prediction,
                probability=probability
            )
            Notification.objects.create(
                recipient=request.user,
                article=article,
                notification_type="flagged",
                message=(
                    f'Your article "{article.title}" '
                    "has been flagged for administrator review."
                )
            )
            messages.warning(
                request,
                "The article was flagged by the AI model and sent to the administrator for review."
            )
        return redirect("/writer/dashboard/")
    return render(
        request,
        "articles/create_article.html",
        {"categories": categories}
    )

@login_required
def article_detail_page(request, pk):
    article = get_object_or_404(
        Article.objects.select_related(
            "author",
            "category"
        ),
        pk=pk
    )
    if (
        article.status != "published"
        and request.user != article.author
        and not request.user.is_superuser
    ):
        messages.error(
            request,
            "You cannot view this article."
        )
        return redirect("/")
    if request.user != article.author:
        article.views += 1
        article.save(
            update_fields=["views"]
        )
    liked = Like.objects.filter(
        user=request.user,
        article=article
    ).exists()
    bookmarked = Bookmark.objects.filter(
        user=request.user,
        article=article
    ).exists()
    return render(
        request,
        "articles/article_detail.html",
        {
            "article": article,
            "liked": liked,
            "bookmarked": bookmarked,
        }
    )

@login_required
def like_article(request, pk):
    if request.method != "POST":
        return redirect("/article/" + str(pk) + "/")
    article = get_object_or_404(
        Article,
        pk=pk,
        status="published"
    )
    like = Like.objects.filter(
        user=request.user,
        article=article
    ).first()
    if like:
        like.delete()
    else:
        Like.objects.create(
            user=request.user,
            article=article
        )
    return redirect(
        "/article/" + str(pk) + "/"
    )

@login_required
def bookmark_article(request, pk):
    if request.method != "POST":
        return redirect("/article/" + str(pk) + "/")
    article = get_object_or_404(
        Article,
        pk=pk,
        status="published"
    )
    bookmark = Bookmark.objects.filter(
        user=request.user,
        article=article
    ).first()
    if bookmark:
        bookmark.delete()
    else:
        Bookmark.objects.create(
            user=request.user,
            article=article
        )
    return redirect(
        "/article/" + str(pk) + "/"
    )