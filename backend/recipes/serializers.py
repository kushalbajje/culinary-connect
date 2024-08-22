from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """
    This serializer is like a master chef that knows how to present our Recipe model
    in a way that's easy for our API to serve up and for others to consume.
    """

    # We're making sure the author field is read-only. 
    # It's like having the chef's signature on the dish - you can see it, but you can't change it!
    author = serializers.ReadOnlyField(source='author.username')

    # The image field is optional. It's like the garnish on a plate - nice to have, but not required.
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        # Here's our menu of fields. We're including everything from the recipe's ID to its image.
        fields = ['id', 'title', 'description', 'ingredients', 'instructions', 
                  'preparation_time', 'cooking_time', 'servings', 'difficulty', 
                  'category', 'cuisine', 'author', 'created_at', 'updated_at', 'image']
        # These fields are for display only - like the date on a wine bottle, you can see it but not change it.
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        """
        This method is like a helpful waiter who brings you a photo of the dish if it's available.
        If there's no photo, they'll just shrug and say 'No image available'.
        """
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

    def create(self, validated_data):
        """
        This is our recipe creation method. It's like following a recipe to create a new dish.
        We take all the ingredients (validated data) and mix them together to create a new Recipe object.
        """
        return Recipe.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        This method is for updating recipes. It's like adjusting a dish to taste.
        We go through each field (attr) and update it with the new value, then save the changes.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# Remember, this serializer is your kitchen assistant. It helps prepare your Recipe data
# for serving via the API, and helps interpret incoming data to create or update recipes.
# Use it wisely in your views, and your API will be serving up delicious data in no time!