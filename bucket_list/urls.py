from django.urls import path
from bucket_list.views import show_bucket_list, delete_bucket_list, edit_bucket_list, show_bucket_list_history, add_bucket_list, remove_from_bucket_list, show_json, get_food

app_name = 'bucket_list'

urlpatterns = [
    path('', show_bucket_list, name='show_bucket_list'),
    path('history', show_bucket_list_history, name='show_bucket_list_history'),
    path('add-bucket-list', add_bucket_list, name='add_bucket_list'),
    path('delete-bucket-list/<uuid:id>', delete_bucket_list, name='delete_bucket_list'),
    path('edit-bucket-list/<uuid:id>', edit_bucket_list, name='edit_bucket_list'),
    path('remove-food/<uuid:food_id>/<uuid:bucket_id>/', remove_from_bucket_list, name='remove_from_bucket_list'),
    path('json/', show_json, name='show_json'),
    path('get-food/<uuid:food_id>/', get_food, name='get_food'),
]
