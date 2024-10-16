from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
    

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    github_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked {self.project.title}'

class Comment(models.Model):
   class Comment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.project.title}'

class Follower(models.Model):
    follower_identifier = models.CharField(max_length=255, default='unknown')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    ip_address = models.GenericIPAddressField(null=True, blank=True) 
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower_identifier} follows {self.followed.username}'
