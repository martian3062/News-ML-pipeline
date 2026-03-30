"""
Custom CORS Middleware — guarantees CORS headers on ALL responses,
including Django 500 error pages where django-cors-headers fails.
"""

from django.utils.deprecation import MiddlewareMixin


ALLOWED_ORIGINS = [
    "https://news-llm.netlify.app",
    "http://news-llm.netlify.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]


class CorsAlwaysMiddleware(MiddlewareMixin):
    """
    Adds CORS headers to EVERY response — even 500 errors.

    django-cors-headers only processes responses that go through the
    normal middleware chain. If a view crashes hard (e.g. import error),
    Django's error handler returns a response that skips CORS.
    This middleware sits very high in the stack and patches the response.
    """

    def process_response(self, request, response):
        origin = request.META.get("HTTP_ORIGIN", "")

        if origin in ALLOWED_ORIGINS:
            # Only add if not already present (don't double up with django-cors-headers)
            if "Access-Control-Allow-Origin" not in response:
                response["Access-Control-Allow-Origin"] = origin
                response["Access-Control-Allow-Credentials"] = "true"
                response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
                response["Access-Control-Allow-Headers"] = (
                    "Accept, Accept-Encoding, Authorization, Content-Type, "
                    "DNT, Origin, User-Agent, X-CSRFToken, X-Requested-With, Range"
                )
                response["Access-Control-Expose-Headers"] = (
                    "Content-Range, Accept-Ranges, Content-Length"
                )

        return response

    def process_request(self, request):
        """Handle preflight OPTIONS requests immediately."""
        if request.method == "OPTIONS":
            origin = request.META.get("HTTP_ORIGIN", "")
            if origin in ALLOWED_ORIGINS:
                from django.http import HttpResponse
                resp = HttpResponse(status=200)
                resp["Access-Control-Allow-Origin"] = origin
                resp["Access-Control-Allow-Credentials"] = "true"
                resp["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
                resp["Access-Control-Allow-Headers"] = (
                    "Accept, Accept-Encoding, Authorization, Content-Type, "
                    "DNT, Origin, User-Agent, X-CSRFToken, X-Requested-With, Range"
                )
                resp["Access-Control-Max-Age"] = "86400"
                return resp

        return None
