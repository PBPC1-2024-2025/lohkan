from django.forms import ModelForm
from food_review.models import ReviewEntry

class ReviewEntryForm(ModelForm):
    class Meta:
        model = ReviewEntry
        fields = ["name", "food_type", "rating", "comments"]