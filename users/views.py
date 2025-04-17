from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.serializers import Serializer, ValidationError
from users import serializers

User = get_user_model()

class UserRegisterationAPIView(GenericAPIView):
    """
    An endpoint for the client to create a new user
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegisterationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response(
            {
                "message": "User registered successfully!",
                "user": serializer.data,
                "tokens": tokens,
            },
            status=status.HTTP_201_CREATED,
        )
    
class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users 
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)

            try:
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data
                serializer = serializers.CustomUserSerializer(user)

            # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                }
            
                return Response(
                    {"message": "Login successful!", "user": serializer.data, "tokens": tokens},
                    status=status.HTTP_200_OK
                )
            except ValidationError as e:

                return Response({"error": e.detail}, status=status.HTTP_401_UNAUTHORIZED)

            
    
class UserLogoutAPIView(GenericAPIView):
    """
    An endpoint to logout users
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = Serializer

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class UserAPIView(RetrieveUpdateAPIView):
    """
    Get, update user information
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user