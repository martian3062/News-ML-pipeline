from rest_framework import serializers
from .models import UserPreference


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ["preferred_categories", "preferred_sources", "blocked_topics",
                  "notification_enabled", "daily_digest_enabled"]
