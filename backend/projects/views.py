from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .serializer_project import *
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User,AnonymousUser
from .models import Profile, Project, Like, Follower, Comment
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import logging
import json

# Create your views here.

# @api_view(['GET'])
# def apiOverview(request):
#     return Response({"message": "Hello from Django API!"})

@api_view(['POST'])
def signup_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password)  
    )

    Profile.objects.create(user=user)

    return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'success': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})

@api_view(['POST'])
def create_or_update_profile(request):
    if not request.user.is_superuser:
        return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

    bio = request.data.get('bio')
    profile_picture = request.data.get('profile_picture')

    profile, created = Profile.objects.get_or_create(user=request.user)  # Handle profile creation
    profile.bio = bio
    profile.profile_picture = profile_picture
    profile.save()

    return Response({'success': 'Profile updated successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_project(request):
    if not request.user.is_superuser:
        return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

    title = request.data.get('title')
    description = request.data.get('description')
    github_url = request.data.get('github_url')

    Project.objects.create(
        owner=request.user,
        title=title,
        description=description,
        github_url=github_url
    )

    return Response({'success': 'Project added successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def is_admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return Response({'is_admin': True}, status=status.HTTP_200_OK)
    return Response({'is_admin': False}, status=status.HTTP_200_OK)



@api_view(['POST'])
def like_project(request, project_id):
    if request.user.is_authenticated:
        project = Project.objects.get(id=project_id)
        if not Like.objects.filter(user=request.user, project=project).exists():
            Like.objects.create(user=request.user, project=project)
            project.like_count += 1
            project.save()
            return Response({'success': 'Liked successfully', 'likes': project.like_count}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You have already liked this project'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def follow_profile(request, username):
    if request.user.is_authenticated:
        admin_user = User.objects.get(username=username)
        if not Follower.objects.filter(follower=request.user, followed=admin_user).exists():
            Follower.objects.create(follower=request.user, followed=admin_user)
            admin_profile = Profile.objects.get(user=admin_user)
            admin_profile.followers_count += 1
            admin_profile.save()
            return Response({'success': 'Followed successfully', 'followers': admin_profile.followers_count}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are already following this profile'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_profile(request):
    try:
        user = request.user
        profile = Profile.objects.get(user=user)
        profile_data = {
            'username': user.username,
            'bio': profile.bio,
            'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
            'followers_count': profile.followers_count
        }
        return Response(profile_data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_comment(request, project_id):
    project = Project.objects.get(id=project_id)
    comment_text = request.data.get('comment')
    
    if not comment_text:
        return Response({'error': 'Comment text is required'}, status=status.HTTP_400_BAD_REQUEST)

    Comment.objects.create(
        user=request.user,
        project=project,
        text=comment_text
    )
    return Response({'success': 'Comment added successfully'}, status=status.HTTP_201_CREATED)
@api_view(['GET'])
def get_projects(request):
    projects = Project.objects.all()  # Fetch all projects
    serialized_projects = ProjectSerializer(projects, many=True)
    return Response(serialized_projects.data, status=status.HTTP_200_OK)

logger = logging.getLogger(__name__)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_unfollow(request):
    logger.info(f"Received follow/unfollow request from user: {request.user}")

    target_user_id = request.data.get('target_user_id')
    
    try:
        target_user = User.objects.get(id=target_user_id)
    except User.DoesNotExist:
        logger.error(f"Target user with id {target_user_id} does not exist.")
        return Response({'error': 'User not found'}, status=404)

    if request.user == target_user:
        logger.error("User tried to follow themselves.")
        return Response({'error': 'You cannot follow yourself'}, status=400)

    follower_relation, created = Follower.objects.get_or_create(follower=request.user, followed=target_user)

    if not created:
        follower_relation.delete()
        target_user.profile.followers_count -= 1
        target_user.profile.save()
        logger.info(f"User {request.user.username} unfollowed {target_user.username}.")
        return Response({'message': 'Unfollowed'}, status=200)
    else:
        target_user.profile.followers_count += 1
        target_user.profile.save()
        logger.info(f"User {request.user.username} followed {target_user.username}.")
        return Response({'message': 'Followed'}, status=200)