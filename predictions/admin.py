from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = [
        "article",
        "prediction",
        "probability",
        "created_at",
    ]
    list_filter = [
        "prediction",
    ]