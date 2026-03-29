from django.urls import path
from .views import GenerateVideoView, VideoStreamView
from .log_view import LogView

urlpatterns = [
    path('generate/', GenerateVideoView.as_view(), name='generate-video'),
    path('stream/<str:filename>/', VideoStreamView.as_view(), name='stream-video'),
    path('logs/', LogView.as_view(), name='logs-view'),
]
