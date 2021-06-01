from django.urls import path
from django.urls import include
from app.api.views.poems import PoemViewSet, GenreViewSet, TopicViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('genres', GenreViewSet, basename='api-genres')
router.register('topics', TopicViewSet, basename='api-topics')
router.register('poems', PoemViewSet, basename='api-poems')

urlpatterns = [
    path('', include(router.urls)),
]
