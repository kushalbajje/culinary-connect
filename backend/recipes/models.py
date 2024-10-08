from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    preparation_time = models.IntegerField(help_text="In minutes", default=0)
    cooking_time = models.IntegerField(help_text="In minutes", default=0)
    servings = models.IntegerField(default=1)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    category = models.CharField(max_length=100, default='Uncategorized')
    cuisine = models.CharField(max_length=100, default='General')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True) 

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None