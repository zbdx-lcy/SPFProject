from django.urls import path
from .views import register_user, login_user, show_info

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('user_info/', show_info, name='show_info'),
]