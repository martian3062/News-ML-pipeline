from rest_framework import serializers
from .models import StoryArc, TimelineEvent


class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = ["id", "title", "description", "event_date", "sentiment", "importance"]


class StoryArcListSerializer(serializers.ModelSerializer):
    event_count = serializers.SerializerMethodField()

    class Meta:
        model = StoryArc
        fields = ["id", "title", "slug", "description", "entities", "image_url",
                  "is_active", "event_count", "created_at"]

    def get_event_count(self, obj):
        return obj.events.count()


class StoryArcDetailSerializer(serializers.ModelSerializer):
    events = TimelineEventSerializer(many=True, read_only=True)

    class Meta:
        model = StoryArc
        fields = ["id", "title", "slug", "description", "entities", "events",
                  "image_url", "is_active", "created_at"]
