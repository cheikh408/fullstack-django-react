from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from core.user.serializers import UserSerializer

class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer used for user authentication and token generation.
    Inherits from TokenObtainPairSerializer provided by rest_framework_simplejwt.
    """

    def validate(self, attrs):
        """
        Validate user credentials and generate JWT tokens.
        """

        # Call parent's validate() method to verify user credentials and generate access and refresh tokens.
        data = super().validate(attrs)

        # Get user data using UserSerializer and add it to the response data.
        data['user'] = UserSerializer(self.user).data

        # Add refresh and access tokens to the response data.
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Update last login time for user if enabled in settings.
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
