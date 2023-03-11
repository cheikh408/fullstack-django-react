from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from core.auth.serializers.register import RegisterSerializer

class RegisterViewSet(ViewSet):
    # Serializer class used to validate and serialize input and output data
    serializer_class = RegisterSerializer
    # Allow any user to access this viewset
    permission_classes = (AllowAny,)
    # Only accept HTTP POST requests
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        # Instantiate a RegisterSerializer object with the request data
        serializer = self.serializer_class(data=request.data)
        # Check if the data is valid, raise an exception if not
        serializer.is_valid(raise_exception=True)
        # Save the validated data to create a new user
        user = serializer.save()
        # Generate a new RefreshToken for the newly created user
        refresh = RefreshToken.for_user(user)
        # Construct a response with the RefreshToken and its corresponding access token
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        # Return a Response object with the serialized user data and the access and refresh tokens
        return Response({
            "user": serializer.data,
            "refresh": res["refresh"],
            "token": res["access"]
        }, status=status.HTTP_201_CREATED)
