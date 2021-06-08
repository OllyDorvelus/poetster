import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _


class AbstractModel(models.Model):
    """Abstract model that handles common fields"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, email, pen_name, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')

        if not pen_name:
            raise ValueError('Please choose a pen name')

        user = self.model(email=self.normalize_email(email), pen_name=pen_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        profile = UserProfile.objects.create(user=user)
        profile.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    pen_name_validator = UnicodeUsernameValidator()

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    pen_name = models.CharField(
        _('pen_name'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[pen_name_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.pen_name

    def like_poem(self, poem):
        user = self
        is_liked = poem.likes.filter(id=user.id).exists()
        poem.likes.remove(user) if is_liked else poem.likes.add(user)
        return not is_liked


class UserProfile(AbstractModel):
    user = models.OneToOneField('User', on_delete=models.PROTECT, related_name='profile')
    subscriptions = models.ManyToManyField('self', blank=True, related_name='subscribers', symmetrical=False)
    bio = models.TextField(blank=True, help_text='A brief description of you.', max_length=500)

    def __str__(self):
        return self.user.pen_name

    # Subscription methods

    @property
    def subscription_count(self):
        return self.subscriptions.exclude(id=self.id).count()

    @property
    def subscriber_count(self):
        return self.subscribers.exclude(id=self.id).count()

    def subscribe(self, user_to_subscribe):
        is_following = self.subscriptions.filter(id=user_to_subscribe.profile.id).exists()
        self.subscriptions.remove(user_to_subscribe.profile) if is_following \
            else self.subscriptions.add(user_to_subscribe.profile)
        return not is_following

    @property
    def poem_count(self):
        return self.user.poems.count()
