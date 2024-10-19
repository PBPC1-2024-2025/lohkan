from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from article.views import (
    create_article, show_xml, show_json, delete_article, 
    show_xml_by_id, show_json_by_id, edit_article, article_detail, add_comment, full_article
)

from .views import index

app_name = 'article'

urlpatterns = [
    path('index/', index, name='index'),
    path('bonus_tdd/', index, name='bonus_tdd'),
    path('article/<uuid:id>/', article_detail, name='article_detail'),
    path('', views.full_article, name='full_article'),
    path('create-article', create_article, name='create_article'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<uuid:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', show_json_by_id, name='show_json_by_id'),
    path('delete/<uuid:id>', delete_article, name='delete_article'),
    path('edit-article/<uuid:id>', edit_article, name='edit_article'), 
    path('article/<uuid:id>/add_comment/', add_comment, name='add_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
