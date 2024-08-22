from django.urls import path
from .views import RecipeListCreateView, RecipeDetailView, CurrentUserRecipeListView, PublicUserRecipeListView, RecipeImageUploadView

# URL patterns for recipe-related API endpoints
urlpatterns = [
    # List all recipes or create a new recipe
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),

    # Retrieve, update, or delete a specific recipe
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),

    # List recipes created by the current authenticated user
    path('my-recipes/', CurrentUserRecipeListView.as_view(), name='my-recipes'),

    # List public recipes for a specific user
    path('users/<str:username>/public-recipes/', PublicUserRecipeListView.as_view(), name='public-user-recipes'),

    # Upload an image for a specific recipe
    path('recipes/<int:pk>/upload-image/', RecipeImageUploadView.as_view(), name='recipe-image-upload'),
]

# Note: Ensure these URLs are included in the main urls.py file, typically under the 'api/' path.