import logging
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework.views import APIView 
from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        existing_user = User.objects.filter(username=username).first()
        
        if existing_user:
            if not existing_user.is_active:
                logger.info(f"Reactivating user: {username}")
                # Reactivate and update the existing inactive user
                for attr, value in serializer.validated_data.items():
                    setattr(existing_user, attr, value)
                existing_user.is_active = True
                existing_user.set_password(serializer.validated_data['password'])
                existing_user.save()
                user = existing_user
                message = "User account reactivated and updated successfully"
                # Create a new token for the reactivated user
                Token.objects.get_or_create(user=user)
            else:
                return Response({"error": "A user with that username already exists and is active."}, 
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.info(f"Creating new user: {username}")
            # Create a new user
            user = serializer.save()
            message = "User account created successfully"
            Token.objects.create(user=user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": message
        }, status=status.HTTP_201_CREATED)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            logger.info(f"User authenticated: {user.username}, is_active: {user.is_active}")
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else:
            username = request.data.get('username')
            user = User.objects.filter(username=username).first()
            if user:
                logger.info(f"Login attempt failed for user: {username}, is_active: {user.is_active}")
            else:
                logger.info(f"Login attempt failed, user not found: {username}")
            return Response({"error": "Unable to log in with provided credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        logger.info(f"Deactivating user: {instance.username}")
        instance.is_active = False
        instance.save()
        # Delete the user's auth token
        Token.objects.filter(user=instance).delete()
        return Response({"message": "User account deactivated successfully."}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)