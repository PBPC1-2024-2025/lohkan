from django.urls import path
from explore.views import show_explore, add_food

app_name = 'explore'

urlpatterns = [
    path('', show_explore, name='show_explore'),
    path('add_food/', add_food, name='add_food'),
]