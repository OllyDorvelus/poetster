from django.db import models
from app.users.models import AbstractModel


class ActiveMixin(models.Model):
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Poem(AbstractModel, ActiveMixin):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='poems')
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, blank=False, related_name='poems')
    topic = models.ManyToManyField('Topic', blank=False, related_name='poems')
    likes = models.ManyToManyField('users.User', related_name='liked', symmetrical=False)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False, max_length=1000)
    about = models.CharField(max_length=150, blank=True, default='')


class Genre(AbstractModel, ActiveMixin):
    name = models.CharField(max_length=55)


class Topic(AbstractModel, ActiveMixin):
    name = models.CharField(max_length=75)
