from rest_framework import viewsets
from app.api.serializers.users import UserSerializer, UserCreateSerializer
from app.users.models import User, UserProfile


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'create':
            serializer_class = UserCreateSerializer
        return serializer_class


