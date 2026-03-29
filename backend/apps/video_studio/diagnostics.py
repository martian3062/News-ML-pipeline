from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import os
from django.conf import settings

class LogView(APIView):
    """Diagnostic view to read backend logs directly from Render ephemeral disk."""
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        log_path = os.path.join(settings.BASE_DIR, 'django_err.log')
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r') as f:
                    content = f.read()[-20000:]
                return Response({'logs': content}, status=200)
            except Exception as e:
                return Response({'error': str(e)}, status=500)
        return Response({'error': f"Log not found at {log_path}"}, status=404)
