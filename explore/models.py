import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.template.defaultfilters import default


class Csv(models.Model):
    file_name = models.FileField(upload_to="csvs")
    upload_date = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    def __str__(self):
        return f"File id: {self.id}"


# Create your models here.
class Food(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    class TypeChoices(models.TextChoices):
        MC = 'MC', 'Main Course'
        DS = 'DS', 'Dessert'
        DR = 'DR', 'Drinks'
        SN = 'SN', 'Snacks'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=20)
    description = models.TextField()
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    image_link = models.URLField(default='')
    type = models.CharField(
        max_length=2,
        choices=TypeChoices.choices,
        default=TypeChoices.MC
    )
    def __str__(self):
        return str(self.name)
