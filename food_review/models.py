from django.db import models
import uuid
from django.contrib.auth.models import User
from explore.models import Food

# Create your models here.
class ReviewEntry(models.Model):
    FOOD_TYPE_CHOICES = [
        ('MC', 'Main Course'),
        ('DS', 'Dessert'),
        ('DR', 'Drinks'),
        ('SN', 'Snacks'),
        # Tambahkan pilihan lain sesuai kebutuhan
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    food_type = models.CharField(max_length=2, choices=FOOD_TYPE_CHOICES)
    rating = models.IntegerField()
    comments = models.TextField()
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE, default=0)