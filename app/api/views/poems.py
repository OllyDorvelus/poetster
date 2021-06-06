from app.poems.models import Poem, Genre, Topic
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
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

    def create(self, request, *args, **kwargs):
        # overriding to return regular poem serializer from create
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(PoemSerializer(instance).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
