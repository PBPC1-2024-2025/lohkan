from django.urls import path
from bucket_list.views import show_bucket_list, add_bucket_list, show_json

app_name = 'bucket_list'

urlpatterns = [
    path('', show_bucket_list, name='show_bucket_list'),
    path('add-bucket-list', add_bucket_list, name='add_bucket_list'),
    path('json/', show_json, name='show_json'),
]
