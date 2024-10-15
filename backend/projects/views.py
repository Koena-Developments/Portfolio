from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer_project import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Profile, Project, Like, Follower, Comment
import logging

logger = logging.getLogger(__name__)

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

@api_view(['POST'])
def create_or_update_profile(request):
    # Allow any user to create/update their profile
    bio = request.data.get('bio')
    profile_picture = request.data.get('profile_picture')

    user = request.data.get('username')  # You can get the username from the request
    profile, created = Profile.objects.get_or_create(user=user)
    profile.bio = bio
    profile.profile_picture = profile_picture
    profile.save()

    return Response({'success': 'Profile updated successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_project(request):
    title = request.data.get('title')
    description = request.data.get('description')
    github_url = request.data.get('github_url')

    Project.objects.create(
        title=title,
        description=description,
        github_url=github_url
    )

    return Response({'success': 'Project added successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_projects(request):
    projects = Project.objects.all()  # Fetch all projects
    serialized_projects = ProjectSerializer(projects, many=True)
    return Response(serialized_projects.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def like_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        # Remove authentication check
        if not Like.objects.filter(user=request.user, project=project).exists():
            Like.objects.create(user=request.user, project=project)
            project.like_count += 1
            project.save()
            return Response({'success': 'Liked successfully', 'likes': project.like_count}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You have already liked this project'}, status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def follow_profile(request, username):
    try:
        admin_user = User.objects.get(username=username)
        if not Follower.objects.filter(follower=request.user, followed=admin_user).exists():
            Follower.objects.create(follower=request.user, followed=admin_user)
            admin_profile = Profile.objects.get(user=admin_user)
            admin_profile.followers_count += 1
            admin_profile.save()
            return Response({'success': 'Followed successfully', 'followers': admin_profile.followers_count}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are already following this profile'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def unfollow_profile(request, username):
    try:
        admin_user = User.objects.get(username=username)
        # Check if the user is already following the profile
        follow_relation = Follower.objects.filter(follower=request.user, followed=admin_user)
        if follow_relation.exists():
            follow_relation.delete()
            admin_profile = Profile.objects.get(user=admin_user)
            admin_profile.followers_count -= 1
            admin_profile.save()
            return Response({'success': 'Unfollowed successfully', 'followers': admin_profile.followers_count}, status=200)
        else:
            return Response({'error': 'You are not following this profile'}, status=400)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

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
def get_profile(request, username=None):
    if username is None:
        username = request.user.username  

    try:
        user = User.objects.get(username=username)
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
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


