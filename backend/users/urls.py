from django.urls import path
from .views import RegisterView, UserDetailView, UserDeleteView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserDetailView.as_view(), name='user-detail'),
    path('delete/', UserDeleteView.as_view(), name='user-delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
]