from django.db import models
import uuid

class Lohkan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)