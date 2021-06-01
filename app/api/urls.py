from django.urls import path
from django.urls import include
from app.api.views.poems import PoemViewSet, GenreViewSet, TopicViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('genres', GenreViewSet)
router.register('topics', TopicViewSet)
router.register('poems', PoemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
