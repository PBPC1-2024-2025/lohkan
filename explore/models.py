import uuid

from django.db import models
from django.db.models import Avg
from django.template.defaultfilters import default


# Create your models here.
class Food(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=20)
    description = models.TextField()
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    image_link = models.URLField(default='')
