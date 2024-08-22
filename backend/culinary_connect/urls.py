"""
URL configuration for culinary_connect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import CustomObtainAuthToken
from django.conf import settings
from django.conf.urls.static import static

# Here's where we define all our URL patterns. Think of it as the table of contents for our API.
urlpatterns = [
    # The admin site - because sometimes we need to roll up our sleeves and dive into the backend
    path('admin/', admin.site.urls),
    
    # All our recipe-related URLs. We're keeping them organized in their own file.
    # It's like having a separate recipe book within our larger cookbook.
    path('api/', include('recipes.urls')),
    
    # This is for logging in. It's using a custom view for handling authentication.
    # Think of it as the bouncer at the entrance of our exclusive cooking club.
    path('api/login/', CustomObtainAuthToken.as_view(), name='api_token_auth'),
    
    # User-related URLs. Again, we're keeping things tidy by putting these in their own file.
    # It's where all the user profile magic happens!
    path('api/users/', include('users.urls')),
]

# This is a neat trick for serving media files during development.
# It's like setting up a temporary art gallery for all our food photos.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Don't forget to add this line to serve static files as well!
# It's like setting up the basic decor of our restaurant before the guests arrive.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)