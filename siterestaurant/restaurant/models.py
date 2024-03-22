from django.db import models
from django.urls import reverse


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Restaurant.Status.PUBLISHED)


# Create your models here.
class Restaurant(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    slug = models.SlugField(max_length=255, db_index=True,
                            unique=True)
    review = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    author = models.TextField(blank=True)
    dish = models.CharField(max_length=100)
    category = models.IntegerField(blank=True)
    photo = models.ImageField(upload_to='restaurant/static/restaurant/images', blank=True)

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    objects = models.Manager()
    published = PublishedModel()

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.author
