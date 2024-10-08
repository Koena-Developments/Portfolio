from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('login/', views.login_view, name='login_api'),
    path('logout/', views.logout_view, name='logout_api'),
]