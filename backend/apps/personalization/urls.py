from django.urls import path
from . import views

urlpatterns = [
    path("feed/", views.personalized_feed, name="personalized-feed"),
    path("trending/", views.trending_topics, name="trending-topics"),
]
