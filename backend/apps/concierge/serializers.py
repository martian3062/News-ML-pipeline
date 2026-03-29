from rest_framework import serializers
from .models import ConversationSession


class ConversationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationSession
        fields = ["id", "messages", "profile_extracted", "products_recommended",
                  "session_type", "started_at"]


class ChatMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    session_id = serializers.UUIDField(required=False)
