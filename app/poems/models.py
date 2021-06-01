from django.db import models
from app.users.models import AbstractModel


class ActiveMixin(models.Model):
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Poem(AbstractModel, ActiveMixin):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='poems')
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, blank=False, related_name='poems')
    topics = models.ManyToManyField('Topic', blank=False, related_name='poems')
    likes = models.ManyToManyField('users.User', related_name='liked')
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False, max_length=1000)
    about = models.CharField(max_length=150, blank=True, default='')

    def __str__(self):
        return f'{self.user} - {self.title}'


class Genre(AbstractModel, ActiveMixin):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class Topic(AbstractModel, ActiveMixin):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name
