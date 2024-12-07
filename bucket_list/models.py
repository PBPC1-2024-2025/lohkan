import uuid
from django.db import models
from django.contrib.auth.models import User
from explore.models import Food

class BucketList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, null=True, blank=True)
    foods = models.ManyToManyField(Food, related_name="bucket_lists")