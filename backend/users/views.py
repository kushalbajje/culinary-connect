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
    """
    User registration view. Handles new user creation and reactivation of inactive users.
    """
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
                user = self._reactivate_user(existing_user, serializer.validated_data)
                message = "ACCOUNT_REACTIVATED"
            else:
                return Response({
                    "status": "error",
                    "code": "ACCOUNT_ALREADY_EXISTS",
                    "message": "A user with that username already exists and is active."
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = serializer.save()
            message = "ACCOUNT_CREATED"
            Token.objects.create(user=user)

        return Response({
            "status": "success",
            "code": message,
            "message": "User account operation successful",
            "data": UserSerializer(user, context=self.get_serializer_context()).data
        }, status=status.HTTP_201_CREATED)

    def _reactivate_user(self, user, validated_data):
        logger.info(f"Reactivating user: {user.username}")
        for attr, value in validated_data.items():
            setattr(user, attr, value)
        user.is_active = True
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.get_or_create(user=user)
        return user

class CustomObtainAuthToken(ObtainAuthToken):
    """
    Custom token-based authentication view. Handles user login and token generation.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            logger.info(f"User authenticated: {user.username}, is_active: {user.is_active}")
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "status": "success",
                "code": "LOGIN_SUCCESSFUL",
                "message": "User authenticated successfully",
                "data": {
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                }
            })
        else:
            username = request.data.get('username')
            user = User.objects.filter(username=username).first()
            logger.info(f"Login attempt failed for user: {username}, {'is_active: ' + str(user.is_active) if user else 'user not found'}")
            return Response({
                "status": "error",
                "code": "INVALID_CREDENTIALS",
                "message": "Unable to log in with provided credentials"
            }, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update user profile information.
    """
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "code": "PROFILE_RETRIEVED",
            "message": "User profile retrieved successfully",
            "data": serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "status": "success",
            "code": "PROFILE_UPDATED",
            "message": "User profile updated successfully",
            "data": serializer.data
        })

class UserDeleteView(generics.DestroyAPIView):
    """
    Deactivate user account. This view soft-deletes the user by setting is_active to False.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        logger.info(f"Deactivating user: {instance.username}")
        instance.is_active = False
        instance.save()
        Token.objects.filter(user=instance).delete()
        return Response({
            "status": "success",
            "code": "ACCOUNT_DEACTIVATED",
            "message": "User account deactivated successfully."
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    """
    User logout view. Deletes the user's authentication token.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response({
            "status": "success",
            "code": "LOGOUT_SUCCESSFUL",
            "message": "User logged out successfully."
        }, status=status.HTTP_200_OK)