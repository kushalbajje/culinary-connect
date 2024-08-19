# Generated by Django 5.1 on 2024-08-19 21:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='category',
            field=models.CharField(default='Uncategorized', max_length=100),
        ),
        migrations.AddField(
            model_name='recipe',
            name='cooking_time',
            field=models.IntegerField(default=0, help_text='In minutes'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='cuisine',
            field=models.CharField(default='General', max_length=100),
        ),
        migrations.AddField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium', max_length=10),
        ),
        migrations.AddField(
            model_name='recipe',
            name='preparation_time',
            field=models.IntegerField(default=0, help_text='In minutes'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='servings',
            field=models.IntegerField(default=1),
        ),
    ]
