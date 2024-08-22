from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe
from .serializers import RecipeSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import SuspiciousOperation

User = get_user_model()

# This permission class is pretty neat. It lets anyone read, but only the author can edit.
# Kinda like a "look, but don't touch" policy for other users.
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

# This view is doing a lot of heavy lifting. It's like the Swiss Army knife for recipes.
# It handles listing all recipes and creating new ones. Plus, it's got all those fancy
# filtering and searching capabilities. Pretty cool, right?
class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'cuisine', 'difficulty']
    search_fields = ['title', 'description', 'ingredients']
    ordering_fields = ['created_at', 'updated_at', 'title']
    parser_classes = (MultiPartParser, FormParser)

    # This method is like a helper in the kitchen. It takes care of saving the recipe
    # and deals with the image if there is one. Neat and tidy!
    def perform_create(self, serializer):
        image = self.request.data.get('image')
        if image:
            file_name = default_storage.save(f"recipe_images/{image.name}", ContentFile(image.read()))
            serializer.save(author=self.request.user, image=file_name)
        else:
            serializer.save(author=self.request.user)

    # This create method is like a strict chef. It checks if we have all the ingredients
    # (fields) before starting to cook (create the recipe). No half-baked recipes allowed!
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": "error",
                "message": "Invalid data provided",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        required_fields = ['title', 'description', 'ingredients', 'instructions', 
                           'preparation_time', 'cooking_time', 'servings', 
                           'difficulty', 'category', 'cuisine']
        
        missing_fields = [field for field in required_fields if field not in request.data]
        
        if missing_fields:
            return Response({
                "status": "error",
                "message": "Missing required fields",
                "missing_fields": missing_fields
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "status": "success",
            "message": "Recipe created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

# This view is like the food photographer of our app. It handles uploading
# and attaching images to our recipes. Making them look delicious!
class RecipeImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        self.check_object_permissions(request, recipe)
        
        image = request.data.get('image')
        if image:
            try:
                file_name = default_storage.save(f"recipe_images/{image.name}", ContentFile(image.read()))
                image_url = default_storage.url(file_name)
                
                recipe.image = file_name
                recipe.save()
                
                return Response({
                    "status": "success",
                    "message": "Image uploaded successfully",
                    "image_url": image_url
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "status": "error",
                    "message": "Error uploading image",
                    "error_details": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "status": "error",
            "message": "No image provided"
        }, status=status.HTTP_400_BAD_REQUEST)

# This view is like a recipe manager. It can show you the recipe details,
# let you tweak the recipe, or even throw it away if you don't like it anymore.
class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def perform_update(self, serializer):
        instance = self.get_object()
        image = self.request.data.get('image')
        
        if image:
            try:
                # Delete the old image if it exists
                if instance.image:
                    default_storage.delete(instance.image.name)
                
                # Save the new image
                file_name = default_storage.save(f"recipe_images/{image.name}", ContentFile(image.read()))
                serializer.save(image=file_name)
            except IOError as e:
                # Handle file system errors
                raise SuspiciousOperation(f"Error handling image file: {str(e)}")
        else:
            serializer.save()

    # This method is for when you want to change up your recipe. Maybe add more salt?
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response({
                "status": "error",
                "message": "Invalid data provided",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.perform_update(serializer)
        except SuspiciousOperation as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": "success",
            "message": "Recipe updated successfully",
            "data": serializer.data
        })

    # This method is for when you really messed up that recipe and just want to forget about it.
    # It's like throwing away a burnt cake, but don't worry, we'll clean up the image too!
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        recipe_title = instance.title
        
        if instance.image:
            try:
                default_storage.delete(instance.image.name)
            except IOError as e:
                # Log the error or handle it as appropriate for your application
                print(f"Error deleting image for recipe '{recipe_title}': {str(e)}")
        
        self.perform_destroy(instance)
        return Response({
            "status": "success",
            "message": f"Recipe '{recipe_title}' deleted successfully"
        }, status=status.HTTP_200_OK)

# This view is like your personal cookbook. It shows all the recipes you've created.
# Great for when you're feeling nostalgic or just can't remember what you cooked last week!
class CurrentUserRecipeListView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'cuisine', 'difficulty']
    search_fields = ['title', 'description', 'ingredients']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

# This view is like peeking into someone else's cookbook, but only the recipes they're willing to share.
# It's a great way to discover new recipes from other users!
class PublicUserRecipeListView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'cuisine', 'difficulty']
    search_fields = ['title', 'description', 'ingredients']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return Recipe.objects.filter(author=user, is_public=True)