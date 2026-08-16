from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from articles.models import Article
from notifications.models import Notification

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("/")
    total_articles = Article.objects.count()
    published_articles = Article.objects.filter(
        status="published"
    ).count()
    flagged_articles = Article.objects.filter(
        status="flagged"
    ).count()
    rejected_articles = Article.objects.filter(
        status="rejected"
    ).count()
    return render(
        request,
        "dashboard/dashboard.html",
        {
            "total_articles": total_articles,
            "published_articles": published_articles,
            "flagged_articles": flagged_articles,
            "rejected_articles": rejected_articles,
        }
    )

@login_required
def flagged_articles(request):
    if not request.user.is_superuser:
        return redirect("/")
    articles = Article.objects.filter(
        status="flagged"
    ).select_related(
        "author",
        "category"
    ).order_by("-created_at")
    return render(
        request,
        "dashboard/flagged_articles.html",
        {
            "articles": articles
        }
    )

@login_required
def review_article(request, pk):

    if not request.user.is_superuser:
        return redirect("/")
    article = get_object_or_404(
        Article,
        pk=pk,
        status="flagged"
    )
    return render(
        request,
        "dashboard/review_article.html",
        {
            "article": article
        }
    )

@login_required
def approve_article(request, pk):
    if not request.user.is_superuser:
        return redirect("/")
    article = get_object_or_404(
        Article,
        pk=pk,
        status="flagged"
    )
    if request.method == "POST":
        comment = request.POST.get(
            "comment",
            "Article approved by administrator."
        )
        article.status = "published"
        article.published_at = timezone.now()
        article.admin_comment = comment
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
        messages.success(
            request,
            "Article approved and published successfully."
        )
        return redirect(
            "/administrator/flagged/"
        )
    return redirect(
        "/administrator/review/"
        + str(pk)
        + "/"
    )

@login_required
def reject_article(request, pk):
    if not request.user.is_superuser:
        return redirect("/")
    article = get_object_or_404(
        Article,
        pk=pk,
        status="flagged"
    )
    if request.method == "POST":
        comment = request.POST.get(
            "comment"
        )
        if not comment:
            comment = "Article rejected by administrator."
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
        messages.success(
            request,
            "Article rejected successfully."
        )
        return redirect(
            "/administrator/flagged/"
        )
    return redirect(
        "/administrator/review/"
        + str(pk)
        + "/"
    )