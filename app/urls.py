from django.urls import path
from app import views
app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('restaurants/<slug:restaurant_slug>/', views.show_restaurant,name='show_restaurant'),
    path('restaurants/<slug:restaurant_slug>/manage', views.manage_restaurant,name='manage_restaurant'),
    path('restaurants/<slug:restaurant_slug>/manage/add_standard_hours', views.add_standard_hours,name='add_standard_hours'),
    path('restaurants/<slug:restaurant_slug>/manage/add_custom_hours', views.add_custom_hours,name='add_custom_hours'),
    path('restaurants/', views.show_restaurants, name='restaurants'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name= 'login'),
    path('logout/', views.user_logout, name='logout'),
]