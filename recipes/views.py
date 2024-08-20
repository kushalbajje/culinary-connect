from django.shortcuts import render
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe
from .serializers import RecipeSerializer

class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'cuisine', 'difficulty']
    search_fields = ['title', 'description', 'ingredients']
    ordering_fields = ['created_at', 'updated_at', 'title']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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

class RecipeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return queryset.filter(author=self.request.user)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        recipe_title = instance.title
        self.perform_destroy(instance)
        return Response({
            "message": f"Recipe '{recipe_title}' deleted successfully"
        }, status=status.HTTP_200_OK)