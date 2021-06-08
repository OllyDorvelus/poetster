from rest_framework import serializers

from app.poems.models import Poem, Genre, Topic
from app.api.serializers.users import UserSerializer

STANDARD_FIELDS = ['id', 'name', 'active']
END_FIELDS = ['created', 'updated']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = STANDARD_FIELDS


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = STANDARD_FIELDS


class PoemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)
    topics = TopicSerializer(read_only=True, many=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Poem
        fields = [
            'id',
            'user',
            'title',
            'genre',
            'content',
            'about',
            'topics',
            'like_count'
        ] + END_FIELDS

    def get_like_count(self, instance):
        return instance.like_count


class PoemCreateSerializer(serializers.ModelSerializer):
    genre_id = serializers.UUIDField()
    topic_ids = serializers.ListField()

    class Meta:
        model = Poem
        fields = [
            'title',
            'content',
            'about',
            'genre_id',
            'topic_ids'
        ]

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        genre_id = validated_data.get('genre_id', None)
        title = validated_data.get('title', None)
        content = validated_data.get('content', None)
        about = validated_data.get('about', None)
        topics_ids = validated_data.get('topics_ids', None)
        new_poem = Poem.objects.create(user=user, genre_id=genre_id, title=title, content=content, about=about)
        if topics_ids is not None:
            new_poem.topics.set(topics_ids)
        return new_poem
