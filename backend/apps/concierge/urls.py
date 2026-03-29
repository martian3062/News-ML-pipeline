from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat, name="concierge-chat"),
    path("session/<uuid:session_id>/", views.get_session, name="concierge-session"),
]
