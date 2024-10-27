from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('authentication.urls')),
    path('article/', include('article.urls')),
    path('food-review/', include('food_review.urls')),
    path('ask_recipe/', include('ask_recipe.urls')),
    path('', include('explore.urls')),
    path('', include('bucket_list.urls'))
]
