from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    # Ensure password is write-only for security
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'bio', 'date_of_birth')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use create_user method to ensure password is hashed
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Handle password updates separately to ensure proper hashing
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # Limit fields for user updates to prevent unintended changes
        fields = ('first_name', 'last_name', 'email', 'bio', 'date_of_birth')

# Note: Ensure proper permissions are set in views to control access to these serializers.