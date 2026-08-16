from django.db import models

# Create your models here.
from django.db import models
class Prediction(models.Model):
    article = models.OneToOneField(
        "articles.Article",
        on_delete=models.CASCADE,
        related_name="prediction_result"
    )
    prediction = models.CharField(
        max_length=20
    )
    probability = models.FloatField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.article.title} - {self.prediction}"