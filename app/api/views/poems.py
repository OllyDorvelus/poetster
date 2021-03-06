from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from app.poems.models import Poem, Genre, Topic
from app.users.models import User
from app.api.serializers.poems import PoemSerializer, GenreSerializer, TopicSerializer, PoemCreateSerializer
from app.api.permissions import UserObjectPermission
from app.api.pagination import StandardResultsSetPagination


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
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        return super(PoemViewSet, self).get_permissions()

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

    # extra routes
    @action(detail=False, methods=['GET'], name='Get your poems', permission_classes=[IsAuthenticated])
    def me(self, request):
        user_poems = Poem.objects.filter(user=request.user)
        poems = PoemSerializer(user_poems, many=True).data
        return Response(poems)

    @action(detail=True, methods=['GET'], name='Like Poem', permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        poem = self.get_object()
        user = request.user
        print(user)
        user.like_poem(poem)
        return Response(PoemSerializer(poem).data)

    @action(detail=False, methods=['GET'], name='Liked poems', permission_classes=[IsAuthenticated])
    def liked(self, request):
        user_id = request.query_params.get('user_id', None)
        if user_id:
            user = User.objects.get(id=user_id)
            poems = user.liked.filter(active=True)
            serialized_poems = PoemSerializer(poems, many=True)
            return Response(serialized_poems.data)
        else:
            return Response({'error': 'User id must be included in param'}, status=status.HTTP_400_BAD_REQUEST)
