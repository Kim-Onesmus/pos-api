from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name='register'),
    path('user_login/', views.login_view, name='login'),
    path('user_logout/', views.logout_view, name='logout'),
    path('refresh_token/', views.refresh_token_view, name='custom_token_refresh'),

    path('categories/', views.category_list_create, name='category-list-create'),
    path('category/<str:pk>/', views.category_detail, name='category-detail'),
] 