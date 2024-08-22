from rest_framework import serializers
from .models import Recipe
from django.conf import settings

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'ingredients', 'instructions', 
                  'preparation_time', 'cooking_time', 'servings', 'difficulty', 
                  'category', 'cuisine', 'author', 'created_at', 'updated_at', 'image', 'image_url']
        read_only_fields = ['author', 'created_at', 'updated_at', 'image_url']

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url
        return None

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        recipe = Recipe.objects.create(**validated_data)
        # The image is now handled in the view, so we don't need to process it here
        return recipe

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # The image is now handled in the view, so we don't need to process it here
        instance.save()
        return instance