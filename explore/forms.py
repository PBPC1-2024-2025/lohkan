from django.forms import ModelForm
from explore.models import Food, Csv

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ["name", "description", "min_price", "max_price", "image_link", "type"]

class CsvForm(ModelForm):
    class Meta:
        model = Csv
        fields = ('file_name',)