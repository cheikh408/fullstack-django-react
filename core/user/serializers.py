from core.abstrait.serializers import AbstractSerializer
from rest_framework import serializers
from core.user.models import User

class UserSerializer(AbstractSerializer):
    
    class Meta:
        # On indique que le serializer utilise le modèle User
        model = User
        # On spécifie les champs du modèle à inclure dans la sérialisation
        fields = ['id', 'username', 'first_name', 'last_name',  'email', 'is_active', 'created', 'updated']
        # On définit le champ 'is_active' en lecture seule
        read_only_fields = ['is_active']
