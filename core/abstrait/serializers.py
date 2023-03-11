from rest_framework import serializers

class AbstractSerializer(serializers.ModelSerializer):
    # On définit la méthode de sérialisation pour l'identifiant unique de l'utilisateur
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    # On définit les champs 'created' et 'updated' en lecture seule
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    