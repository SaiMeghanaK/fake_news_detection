from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name

class Article(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("published", "Published"),
        ("flagged", "Flagged"),
        ("rejected", "Rejected"),
    )
    PREDICTION_CHOICES = (
        ("real", "Real"),
        ("fake", "Fake"),
        ("pending", "Pending"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles"
    )
    title = models.CharField(
        max_length=255
    )
    content = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles"
    )
    image = models.ImageField(
        upload_to="articles/",
        blank=True,
        null=True
    )
    prediction = models.CharField(
        max_length=20,
        choices=PREDICTION_CHOICES,
        default="pending"
    )
    prediction_probability = models.FloatField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    admin_comment = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True
    )
    views = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "article")

class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "article")