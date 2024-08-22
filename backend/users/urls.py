from django.urls import path
from .views import RegisterView, UserDetailView, UserDeleteView, LogoutView

urlpatterns = [
    # User registration endpoint
    path('register/', RegisterView.as_view(), name='register'),

    # Retrieve or update user profile
    path('profile/', UserDetailView.as_view(), name='user-detail'),

    # Delete user account
    path('delete/', UserDeleteView.as_view(), name='user-delete'),

    # User logout endpoint
    path('logout/', LogoutView.as_view(), name='logout'),
]

# Note: Ensure these URLs are included in the main urls.py file, typically under the 'api/users/' path.