from django.forms import ModelForm
from explore.models import Food

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ["name", "description", "min_price", "max_price", "image_link"]