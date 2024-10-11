from django.contrib import admin
from .models import Profile, Project, Like, Comment, Follower

# Register your models here
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follower)
