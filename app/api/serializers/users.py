from rest_framework import serializers
from app.users.models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'bio'
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    subscriber_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'pen_name',
            'profile',
            'subscriber_count',
        ]

    def get_subscriber_count(self, instance):
        count = -1
        if instance.profile:
            count = instance.profile.subscriber_count
        return count
