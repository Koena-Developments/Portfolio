from django.urls import path
from . import views

urlpatterns = [
    path('api/signup/', views.signup_view, name="signup_api"),
     path('api/profile/<str:username>/', views.get_profile, name='get_profile'),
    path('api/projects/', views.get_projects, name='get_projects'),
    # path('api/follow/', views.follow_unfollow, name='follow_unfollow'),
    path('api/add_project/', views.add_project, name='add_project'),
    path('api/like_project/<int:project_id>/', views.like_project, name='like_project'),
    path('api/unfollow/<str:username>/', views.unfollow_profile, name='unfollow_profile'),
    path('api/add_comment/<int:project_id>/', views.add_comment, name='add_comment'),
    path('api/follow/<str:username>/', views.follow_profile, name='follow_profile'),
    path('api/unfollow/<str:username>/', views.unfollow_profile, name='unfollow_profile'),
]

