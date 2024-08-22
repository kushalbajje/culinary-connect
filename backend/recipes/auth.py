from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):
    """
    This class is like our friendly bouncer at the door of our exclusive API club.
    It checks if you're on the list (i.e., have valid credentials) and gives you a VIP pass (token) if you are.
    """

    def post(self, request, *args, **kwargs):
        # First, we need to check your ID (validate your credentials)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # If your ID checks out, we get your user profile
        user = serializer.validated_data['user']
        
        # Now, let's get you a VIP pass (token). If you already have one, we'll just reuse it
        token, created = Token.objects.get_or_create(user=user)
        
        # Here's your welcome package: your VIP pass (token), your unique identifier (user_id),
        # and a way to contact you (email)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

# Don't forget to use this class in your urls.py instead of the default ObtainAuthToken
# It's like upgrading from a regular bouncer to one that remembers your name and favorite drink!