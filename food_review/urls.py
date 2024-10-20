from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from food_review.views import (
    add_review_ajax, show_xml, show_json, 
    show_xml_by_id, show_json_by_id, index
)
from food_review.views import add_review_ajax

app_name = 'food_review'

urlpatterns = [
    path('food-review', index, name='food_review'),
    path('', views.page_review, name='page_review'),
    path('add-review', add_review_ajax, name='add_review_ajax'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<uuid:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', show_json_by_id, name='show_json_by_id'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)