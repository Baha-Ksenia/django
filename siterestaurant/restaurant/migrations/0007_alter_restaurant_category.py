# Generated by Django 4.2.1 on 2024-03-20 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_remove_restaurant_time_update_restaurant_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='category',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]