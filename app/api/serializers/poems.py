from rest_framework import serializers

from app.poems.models import Poem, Genre, Topic

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
    class Meta:
        model = Poem
        fields = [
            'id',
            'title',
            'genre'
            'user',
            'content',
            'about',
            'topics'
        ] + END_FIELDS
