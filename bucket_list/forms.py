from django.forms import ModelForm
from main.models import BucketList

class BucketListForm(ModelForm):
    class Meta:
        model = BucketList
        fields = ["name"]