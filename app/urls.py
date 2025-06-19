from django.urls import path
from . import views

urlpatterns = [
    path('inventory_login/', views.login_view, name='login'),
    path('refresh_token/', views.refresh_token_view, name='custom_token_refresh'),
] 