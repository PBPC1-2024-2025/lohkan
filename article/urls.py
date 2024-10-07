from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from article.views import create_article, show_xml, show_json

app_name = 'article'

urlpatterns = [
    path('', views.full_article, name='full_article'), 
    path('create-article', create_article, name='create_article'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
