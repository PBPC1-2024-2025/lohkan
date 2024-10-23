from django.forms import ModelForm
from bucket_list.models import BucketList

class BucketListForm(ModelForm):
    class Meta:
        model = BucketList
        fields = ["name"]