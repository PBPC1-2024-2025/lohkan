import uuid

from django.db import models

# Create your models here.
class Food(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    description = models.TextField()
    min_price = models.IntegerField()
    max_price = models.IntegerField()