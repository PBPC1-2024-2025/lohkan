from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from explore.views import show_explore, add_food, edit_food, delete_food, show_xml, add_food_ajax, show_json, search_food, all_to_json, filter_food, upload_file, add_to_bucket_list

app_name = 'explore'

urlpatterns = [
    path('', show_explore, name='show_explore'),
    path('add-food/', add_food, name='add_food'),
    path('edit-food/<uuid:id>', edit_food, name='edit_food'),
    path('delete-food/<uuid:id>', delete_food, name='delete_food'),
    path('xml/', show_xml, name='show_xml'),
    path('add-food-ajax/', add_food_ajax, name='add_food_ajax'),
    path('json/', show_json, name='show_json'),
    path('search-food/', csrf_exempt(search_food), name='search_food'),
    path('all-to-json/', csrf_exempt(all_to_json), name='all_to_json'),
    path('filter-food/', csrf_exempt(filter_food), name='filter_food'),
    path('upload-file/', upload_file, name='upload_file'),
    path('add-to-bucket-list/<uuid:food_id>/<uuid:bucket_id>/', add_to_bucket_list, name='add_to_bucket_list'),
]