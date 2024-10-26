from django.forms import ModelForm
from article.models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "description", "image"]