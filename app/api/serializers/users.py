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


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    password2 = serializers.CharField(min_length=8, trim_whitespace=False, style={'input_type': 'password'},
                                      write_only=True)
    email2 = serializers.EmailField(trim_whitespace=True, style={'input_type': 'email'}, write_only=True)

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8, 'style': {'input_type': 'password'}}}
        fields = ('email', 'email2', 'pen_name', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        email = attrs.get('email')
        email2 = attrs.get('email2')

        if password != password2:
            msg = {'password2': ['Passwords must match.']}
            raise serializers.ValidationError(msg)

        if email != email2:
            msg = {'email2': ['Emails must match.']}
            raise serializers.ValidationError(msg)

        return attrs

    def create(self, validated_data):
        """"Create a new user with encrypted password and return it"""
        del validated_data['password2']
        del validated_data['email2']
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
