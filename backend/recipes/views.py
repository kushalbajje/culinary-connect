from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe
from .serializers import RecipeSerializer
from django.contrib.auth import get_user_model
from .utils import upload_to_s3
from rest_framework.views import APIView
from django.core.files.base import ContentFile
import base64
User = get_user_model()

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'cuisine', 'difficulty']
    search_fields = ['title', 'description', 'ingredients']
    ordering_fields = ['created_at', 'updated_at', 'title']
    parser_classes = (MultiPartParser, FormParser)
    
    def perform_create(self, serializer):
        image = self.request.data.get('image')
        image_url = None
        if image:
            try:
                if isinstance(image, str) and image.startswith('data:image'):
                    # Base64 encoded image - decode it
                    format, imgstr = image.split(';base64,')
                    ext = format.split('/')[-1]
                    data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')
                else:
                    # Regular file upload
                    data = image

                # Upload to S3
                image_url = upload_to_s3(data, f"recipe_images/{data.name}")
            except Exception as e:
                print(f"Error uploading image: {str(e)}")
                # You might want to raise an exception here or handle it as per your requirement

        serializer.save(author=self.request.user, image_url=image_url)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        required_fields = ['title', 'description', 'ingredients', 'instructions', 
                           'preparation_time', 'cooking_time', 'servings', 
                           'difficulty', 'category', 'cuisine']
        
        missing_fields = [field for field in required_fields if field not in request.data]
        
        if missing_fields:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class RecipeImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        self.check_object_permissions(request, recipe)
        
        image = request.data.get('image')
        if image:
            try:
                image_url = upload_to_s3(image, f"recipe_images/{image.name}")
                if image_url:
                    recipe.image_url = image_url
                    recipe.save()
                    return Response({'message': 'Image uploaded successfully', 'image_url': image_url}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Failed to upload image'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({'message': f'Error uploading image: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def perform_update(self, serializer):
        image = self.request.data.get('image')
        if image:
            image_url = upload_to_s3(image, f"recipe_images/{image.name}")
            serializer.save(image_url=image_url)
        else:
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        recipe_title = instance.title
        self.perform_destroy(instance)
        return Response({
            "message": f"Recipe '{recipe_title}' deleted successfully"
        }, status=status.HTTP_200_OK)

class CurrentUserRecipeListView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'cuisine', 'difficulty']
    search_fields = ['title', 'description', 'ingredients']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

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

