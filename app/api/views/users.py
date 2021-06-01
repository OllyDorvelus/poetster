from rest_framework import viewsets
from app.api.serializers.users import UserSerializer
from app.users.models import User, UserProfile


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
