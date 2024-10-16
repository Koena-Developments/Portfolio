from rest_framework import serializers
from .models import Project, Like

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'  

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Like.objects.filter(user=user, project=obj).exists()
        ip = self.context['request'].META.get('REMOTE_ADDR')
        return Like.objects.filter(ip_address=ip, project=obj).exists()
    