from rest_framework import serializers
from .models import VideoProject


class VideoProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProject
        fields = ["id", "title", "slug", "status", "video_url", "thumbnail_url",
                  "duration_seconds", "created_at"]
