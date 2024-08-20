from django.urls import path
from .views import RecipeListCreateView, RecipeDetailView, CurrentUserRecipeListView, PublicUserRecipeListView


urlpatterns = [
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
   path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('my-recipes/', CurrentUserRecipeListView.as_view(), name='my-recipes'),
    path('users/<str:username>/public-recipes/', PublicUserRecipeListView.as_view(), name='public-user-recipes'),
]