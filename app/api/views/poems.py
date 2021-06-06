from app.poems.models import Poem, Genre, Topic
from rest_framework import viewsets
from app.api.serializers.poems import PoemSerializer, GenreSerializer, TopicSerializer, PoemCreateSerializer
from app.api.permissions import UserObjectPermission


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only viewset for genres. Genres are set and will not be suggested by end users.
    """
    queryset = Genre.objects.filter(active=True)
    serializer_class = GenreSerializer


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Topics right now will be set but that can change later on. This can be used as tags and suggested.
    """
    queryset = Topic.objects.filter(active=True)
    serializer_class = TopicSerializer


class PoemViewSet(viewsets.ModelViewSet):
    """
    CRUD actions for poems.
    """
    serializer_class = PoemSerializer
    queryset = Poem.objects.filter(active=True)
    permission_classes = [UserObjectPermission]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'create':
            serializer_class = PoemCreateSerializer
        return serializer_class
