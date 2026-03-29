from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import StoryArc
from .serializers import StoryArcListSerializer, StoryArcDetailSerializer


class StoryArcViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StoryArc.objects.all()
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StoryArcDetailSerializer
        return StoryArcListSerializer
