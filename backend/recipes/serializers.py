from rest_framework import serializers
from .models import Recipe
from culinary_connect import settings
class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'ingredients', 'instructions', 
                  'preparation_time', 'cooking_time', 'servings', 'difficulty', 
                  'category', 'cuisine', 'author', 'created_at', 'updated_at', 'image', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{obj.image.name}"
        return None