from django.urls import path
from explore.views import show_explore

app_name = 'main'

urlpatterns = [
    path('', show_explore, name='explore'),
]