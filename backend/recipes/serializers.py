from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'ingredients', 'instructions', 
                  'preparation_time', 'cooking_time', 'servings', 'difficulty', 
                  'category', 'cuisine', 'author', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']