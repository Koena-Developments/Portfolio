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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@api_view(['POST'])
def create_or_update_profile(request):
    bio = request.data.get('bio')
    profile_picture = request.data.get('profile_picture')

    user = request.data.get('username')  
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
    projects = Project.objects.all()
    serialized_projects = ProjectSerializer(projects, many=True, context={'request': request})
    return Response(serialized_projects.data, status=status.HTTP_200_OK)
@api_view(['POST'])
def like_unlike_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    ip = get_client_ip(request)

    if request.user.is_authenticated:
        like = Like.objects.filter(user=request.user, project=project).first()
        if like:
            # Unlike logic
            like.delete()
            project.like_count -= 1
            project.save()
            return Response({'success': 'Unliked successfully', 'likes': project.like_count}, status=status.HTTP_200_OK)
        else:
            # Like logic
            Like.objects.create(user=request.user, project=project)
            project.like_count += 1
            project.save()
            return Response({'success': 'Liked successfully', 'likes': project.like_count}, status=status.HTTP_200_OK)
    else:
        like = Like.objects.filter(ip_address=ip, project=project).first()
        if like:
            # Unlike logic for anonymous user
            like.delete()
            project.like_count -= 1
            project.save()
            return Response({'success': 'Unliked successfully', 'likes': project.like_count}, status=status.HTTP_200_OK)
        else:
            Like.objects.create(ip_address=ip, project=project)
            project.like_count += 1
            project.save()
            return Response({'success': 'Liked successfully', 'likes': project.like_count}, status=status.HTTP_200_OK)

@api_view(['POST'])
def follow_profile(request, username):
    ip = get_client_ip(request)
    try:
        admin_user = User.objects.get(username=username)
        follower_identifier = request.user.username if request.user.is_authenticated else f'Anonymous_{ip}'

        if Follower.objects.filter(follower_identifier=follower_identifier, followed=admin_user).exists():
            return Response({'error': 'Already following'}, status=status.HTTP_400_BAD_REQUEST)

        Follower.objects.create(follower_identifier=follower_identifier, followed=admin_user, ip_address=ip)

        admin_profile = Profile.objects.get(user=admin_user)
        admin_profile.followers_count += 1
        admin_profile.save()

        return Response(
            {'success': 'Followed successfully', 'followers': admin_profile.followers_count},
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def unfollow_profile(request, username):
    ip = get_client_ip(request)
    try:
        admin_user = User.objects.get(username=username)
        follower_identifier = request.user.username if request.user.is_authenticated else f'Anonymous_{ip}'

        follower_record = Follower.objects.filter(follower_identifier=follower_identifier, followed=admin_user).first()
        if not follower_record:
            return Response({'error': 'Not following this profile'}, status=status.HTTP_400_BAD_REQUEST)

        follower_record.delete()

        admin_profile = Profile.objects.get(user=admin_user)
        admin_profile.followers_count -= 1
        admin_profile.save()

        return Response(
            {'success': 'Unfollowed successfully', 'followers': admin_profile.followers_count},
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_comment(request, project_id):
    ip = get_client_ip(request)
    project = Project.objects.get(id=project_id)
    comment_text = request.data.get('comment')

    if not comment_text:
        return Response({'error': 'Comment text is required'}, status=status.HTTP_400_BAD_REQUEST)

    if request.user.is_authenticated:
        Comment.objects.create(user=request.user, project=project, text=comment_text)
    else:
        Comment.objects.create(ip_address=ip, project=project, text=comment_text)

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


