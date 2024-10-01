from django.forms import ModelForm
from main.models import FoodEntry

class FoodEntryForm(ModelForm):
    class Meta:
        model = FoodEntry
        fields = ["nama", "deskripsi", "harga"]