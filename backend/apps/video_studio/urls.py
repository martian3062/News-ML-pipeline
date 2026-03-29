from django.urls import path
from .views import GenerateVideoView, VideoStreamView

urlpatterns = [
    path('generate/', GenerateVideoView.as_view(), name='generate-video'),
    path('stream/<str:filename>/', VideoStreamView.as_view(), name='stream-video'),
]
