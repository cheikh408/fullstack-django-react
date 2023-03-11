from rest_framework import serializers
from core.user.serializers import UserSerializer
from core.user.models import User

class RegisterSerializer(UserSerializer):
  
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=True,
        help_text="Password must be at least 8 characters and no longer than 128 characters."
    )
    
    class Meta:
        model = User
        fields = ['id',  'email', 'username', 'first_name', 'last_name', 'password']
    
    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier for
        # the UserManager to create a new user.
        return User.objects.create_user(**validated_data)
