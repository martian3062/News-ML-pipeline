from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Translation, SUPPORTED_LANGUAGES
from .serializers import TranslationSerializer


class TranslationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Translation.objects.select_related("source_article").all()
    serializer_class = TranslationSerializer
    permission_classes = [AllowAny]
    filterset_fields = ["language"]


@api_view(["GET"])
@permission_classes([AllowAny])
def supported_languages(request):
    return Response([{"code": code, "name": name} for code, name in SUPPORTED_LANGUAGES])
