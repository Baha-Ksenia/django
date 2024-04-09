from django.contrib import admin
from django.core.checks import messages

# Register your models here.
from .models import Restaurant, Category


class PublicFilter(admin.SimpleListFilter):
    title = 'Наличие контактов'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [('contact_no', 'Нет контактов'), ('contact_yes', 'Есть контакты'), ]

    def queryset(self, request, queryset):
        if self.value() == 'contact_yes':
            return queryset.filter(contact__isnull=False)
        elif self.value() == 'contact_no':
            return queryset.filter(contact__isnull=True)


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('author', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('author',)
    list_editable = ('is_published', 'cat')
    ordering = ['time_create', 'author']
    list_per_page = 10
    actions = ['set_published', 'set_draft']
    search_fields = ['author', 'cat__name']
    list_filter = [PublicFilter, 'cat', 'is_published']
    fields = ['author', 'review', 'slug', 'cat', 'dish', 'tags']
    readonly_fields = ['slug']
    filter_horizontal = ['tags']
    # exclude = ['tags', 'is_published', 'time_create']
    # prepopulated_fields = {"slug": ("dish",)}

    @admin.display(description="Краткое описание", ordering='content')
    def brief_info(self, restaurant: Restaurant):
        return f"Описание {len(restaurant.review)} символов."

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Restaurant.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Restaurant.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)


admin.site.register(Restaurant, RestaurantAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
