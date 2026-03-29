from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Briefing
from .serializers import BriefingListSerializer, BriefingDetailSerializer


class BriefingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Briefing.objects.all()
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BriefingDetailSerializer
        return BriefingListSerializer
