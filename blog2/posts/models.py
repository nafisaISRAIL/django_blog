from __future__ import unicode_literals

from django.db import models
from django.conf import settings


GENDER = (
    (True, 'Female'),
    (False, 'Male'),
)

STATUS = (
    ('p', 'Published'),
    ('d', 'Draft'),
)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='p')


class Author(models.Model):
    gender = models.BooleanField(choices=GENDER, default=True)
    birth = models.DateField(auto_now=False)
    biography = models.TextField(blank=True)
    image = models.ImageField(upload_to='authors',
                              blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                blank=True, null=True)

    def __unicode__(self):
        first_name = self.user.first_name
        last_name = self.user.last_name

        return '{} {}'.format(first_name, last_name)


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(Author)
    category = models.ManyToManyField(Category, null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateField(auto_now=True)
    status = models.CharField(max_length=1,
                              choices=STATUS,
                              default=STATUS[0][0]

                              )
    image = models.ImageField(upload_to='posts', null=True, blank=True)

    published = PublishedManager()
    objects = models.Manager()

    def change_status(self):
        if self.status == 'p':
            self.status = 'd'
        else:
            self.status = 'p'
        self.save()
