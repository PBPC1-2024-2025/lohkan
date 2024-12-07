from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path("register/", register_user, name="register_user"),
    path("login/", login_user, name="login_user"),
    path('logout/', logout_user, name='logout_user'),
    path('web/login/', login, name="login"),
    path('web/logout/', logout, name="logout"),
    path('web/register/', register, name="register"),
]