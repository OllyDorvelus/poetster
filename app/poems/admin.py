from django.contrib import admin
from app.poems import models


# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    fields = ['name', 'active']

    class Meta:
        model = models.Genre


class TopicAdmin(admin.ModelAdmin):
    fields = ['name', 'active']

    class Meta:
        model = models.Topic


class PoemAdmin(admin.ModelAdmin):
    fields = ['user', 'title', 'genre', 'content', 'topics', 'likes', 'active']

    class Meta:
        model = models.Poem


admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Poem, PoemAdmin)
