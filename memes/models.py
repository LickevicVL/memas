from time import time

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from os.path import join, dirname, basename
from memes.utils import TimeAgo


class Mem(models.Model):
    title = models.CharField(max_length=256, db_index=True)
    body = models.TextField(blank=True, db_index=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        default=None,
        upload_to=lambda mem, name: join(
            dirname(basename(__file__)), Mem.__name__, name
        )
            )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_created_at(self):
        return TimeAgo.get_time_ago(self.created_at)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title.lower()) + str(int(time()))

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('memes:mem', kwargs={'slug': self.slug})
