from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.forms import ModelForm
from enum import Enum


class User(models.Model):
    """
    Model whose primary purpose is to display user's profile data.
    """
    user_name = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user')
    first_name = models.CharField(max_length=50, null=True, help_text='Enter your name')
    surname = models.CharField(max_length=50, null=True, help_text='Enter your surname')
    email = models.EmailField()
    user_photo = models.ImageField(upload_to='users', blank=True)
    is_active = models.BooleanField(null=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.surname)


class Community(models.Model):
    """
    Model whose primary purpose is to display Community's data.
    """
    name = models.CharField(max_length=100, null=True, help_text='Enter community name')
    desc = models.CharField(max_length=200, null=True, help_text='Enter community description')
    semantic_tag = models.CharField(max_length=500, null=True, help_text='Enter related semantic tag')
    slug = models.SlugField(max_length=100, null=True)
    community_photo = models.ImageField(upload_to='communities')
    owner = models.ForeignKey(User, related_name='owners', on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(User, related_name='members', help_text='Community members')
    is_active = models.BooleanField(null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name


class PostType(models.Model):
    name = models.CharField(max_length=100, null=True, help_text='Enter post type name')
    desc = models.CharField(max_length=1200, null=True, help_text='Enter post type description')
    related_community = models.ForeignKey(Community,
                                          related_name='related_communities',
                                          on_delete=models.SET_NULL,
                                          null=True)
    semantic_tag = models.CharField(max_length=500, null=True, help_text='Enter related semantic tag')
    semantic_code = models.CharField(max_length=20, null=True, help_text='Enter related semantic tag')
    is_active = models.BooleanField(null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name


class PostTypeObject(models.Model):
    name = models.CharField(max_length=200)
    community = models.ForeignKey(Community, on_delete=models.PROTECT)
    fields = JSONField()
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    related_community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True)
    related_post_type = models.ForeignKey(PostType, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, null=True, help_text='Enter title of post as text')
    body = models.CharField(max_length=200, null=True, help_text='Enter body of post as text')
    semantic_tag = models.CharField(max_length=100, null=True, help_text='Tag comes from related community tag')
    slug = models.SlugField(max_length=100, null=True)
    is_active = models.BooleanField(null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    publish_date = models.DateTimeField(null=True)

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class PostDetails(models.Model):
    related_post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    data = JSONField()

    # JSON field will have all the data fields defined by Community Owner.

    def __str__(self):
        return self.data
