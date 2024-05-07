from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, Contact, TagPost, Restaurant
from django.core.validators import MinLengthValidator, MaxLengthValidator


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789 - "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Изображение")


class AddPollForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    is_published = forms.BooleanField(initial=True, label='Опубликовано')

    class Meta:
        model = Restaurant
        # fields = '__all__'
        fields = ['dish', 'review', 'is_published',
                  'cat', 'author', 'tags', 'contact', 'photo']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-input'}),
            'review': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_review(self):
        review = self.cleaned_data['review']
        if len(review) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return review