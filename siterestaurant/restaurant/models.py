from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
         'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
         'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
         'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh',
         'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r',
         'ю': 'yu', 'я': 'ya'}
    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Restaurant.Status.PUBLISHED)


# Create your models here.
class Restaurant(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    review = models.TextField(blank=True, verbose_name="Отзыв")
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Категории")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время публикации")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус")
    author = models.TextField(blank=True, verbose_name="Автор")
    dish = models.CharField(max_length=100, verbose_name="Блюдо")
    # category = models.IntegerField(blank=True, verbose_name="Категории")
    # photo = models.ImageField(upload_to='images/', blank=True, verbose_name="Фото")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True,
                              null=True, verbose_name="Фото")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Теги")
    contact = models.OneToOneField('Contact', on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='restaurant', verbose_name="Контакты")

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'

    objects = models.Manager()
    published = PublishedModel()

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(translit_to_eng(self.dish))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.author


class Category(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

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


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
