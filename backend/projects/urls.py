from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from . import views

# urlpatterns = [
# ]

urlpatterns = [
    path('api/', views.apiOverview, name="api-overview"),
    path('api/login/', views.login_view, name='login_api'),
    path('api/logout/', views.logout_view, name='logout_api'),
    path('api/signup/', views.signup_view, name="signup_api"),
]