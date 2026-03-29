from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("translations", views.TranslationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("languages/", views.supported_languages, name="supported-languages"),
]
