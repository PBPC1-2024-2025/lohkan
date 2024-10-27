from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class ReviewEntry(models.Model):
    # Updated choices to use full names directly
    FOOD_TYPE_CHOICES = [
        ('Main Course', 'Main Course'),
        ('Dessert', 'Dessert'),
        ('Drinks', 'Drinks'),
        ('Snacks', 'Snacks')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    food_type = models.CharField(max_length=50, choices=FOOD_TYPE_CHOICES)
    rating = models.IntegerField()
    comments = models.TextField()
    