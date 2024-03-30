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

    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    review = models.TextField(blank=True)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    author = models.TextField(blank=True)
    dish = models.CharField(max_length=100)
    category = models.IntegerField(blank=True)
    photo = models.ImageField(upload_to='images/', blank=True)
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')
    contact = models.OneToOneField('Contact', on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='restaurant')

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


class Category(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True)
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name


class TagPost(models.Model):
    tag = models.CharField(max_length=100,
                           db_index=True)
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag


class Contact(models.Model):
    mail = models.CharField(max_length=100)
    phone = models.IntegerField(null=True)

    def __str__(self):
        return self.mail
