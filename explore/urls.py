from django.urls import path
from explore.views import show_explore, add_food, edit_food, delete_food, show_xml

app_name = 'explore'

urlpatterns = [
    path('explore', show_explore, name='show_explore'),
    path('add_food/', add_food, name='add_food'),
    path('edit_food/<uuid:id>', edit_food, name='edit_food'),
    path('delete_food/<uuid:id>', delete_food, name='delete_food'),
    path('xml/', show_xml, name='show_xml'),
]