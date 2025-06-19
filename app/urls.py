from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name='register'),
    path('user_login/', views.login_view, name='login'),
    path('refresh_token/', views.refresh_token_view, name='custom_token_refresh'),
] 