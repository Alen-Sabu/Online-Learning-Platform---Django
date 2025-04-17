from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer to class to serializer CustomUser
    """
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "first_name", "last_name", "profile_picture")  # Add other fields if needed
        extra_kwargs = {
            "email": {"read_only": True},  # Prevent email modification if necessary
        }

class UserRegisterationSerializer(serializers.ModelSerializer):
    """
    Serializer class for user registeration
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class for user login either using email or username
    """
    email = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):

        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email = email, password = password)
            if user and user.is_active:
                return user
            else:
                
                raise serializers.ValidationError("Incorrect credentials")
        else:
            raise serializers.ValidationError("Both the fields are required")


