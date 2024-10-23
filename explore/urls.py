from django.urls import path
from explore.views import show_explore

app_name = 'explore'

urlpatterns = [
    path('', show_explore, name='show_explore'),
]