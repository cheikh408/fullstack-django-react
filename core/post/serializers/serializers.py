# Import des modules nécessaires
from rest_framework import serializers 
from rest_framework.exceptions import ValidationError 
from core.abstrait.serializers import AbstractSerializer 
from core.post.models import Post 
from core.user.models import User

# Définition du sérialiseur pour la classe Post
class PostSerializer(AbstractSerializer):
    # Champ pour spécifier l'auteur du post
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='public_id'
    )

    # Validation du champ author
    def validate_author(self, value):
        # Vérifie si l'utilisateur qui crée le post est bien l'utilisateur spécifié dans le champ author
        if self.context["request"].user != value:
            # Si ce n'est pas le cas, lève une exception de validation avec un message d'erreur
            raise ValidationError("Vous ne pouvez pas créer de message pour un autre utilisateur.")

    # Configuration du sérialiseur
    class Meta:
        # Spécifie le modèle sur lequel se base le sérialiseur
        model = Post
        # Liste des champs à inclure dans une requête ou une réponse
        fields = ['id', 'author', 'body', 'edited', 'created', 'updated']
        # Liste des champs en lecture seule qui ne peuvent pas être modifiés par une requête
        read_only_fields = ["edited"]


      # La méthode update est appelée lorsqu'un objet de modèle est mis à jour à partir des données du formulaire soumis par l'utilisateur.
    def update(self, instance, validated_data):
        
        # Vérifier si l'objet a été modifié en ajoutant une clé "edited" au dictionnaire validated_data
        if not instance.edited:
            validated_data['edited'] = True
        
        # Appeler la méthode parente update pour mettre à jour l'objet de modèle avec les données validées fournies par l'utilisateur
        instance = super().update(instance, validated_data)
        
        # Retourner l'objet mis à jour
        return instance   


     # Champ booléen qui indique si l'utilisateur actuel a aimé le post ou non
    liked = serializers.SerializerMethodField()
    # Champ entier qui contient le nombre de likes qu'un post a reçus
    likes_count = serializers.SerializerMethodField()

    def get_liked(self, instance):
        """Renvoie True si l'utilisateur actuel a aimé le post, sinon False"""
        # Obtient la requête de l'utilisateur actuel depuis self.context
        request = self.context.get('request', None)
        # Vérifie si la requête est None ou si l'utilisateur est anonyme
        if request is None or request.user.is_anonymous:
            # Si la requête est None ou si l'utilisateur est anonyme, renvoie False
            return False
        # Utilise la méthode has_liked de l'utilisateur pour savoir si l'utilisateur a aimé le post
        return request.user.has_liked(instance)

    def get_likes_count(self, instance):
        """Renvoie le nombre de personnes qui ont aimé le post"""
        # Utilise la propriété liked_by de la classe Post pour compter le nombre de personnes qui ont aimé le post
        return instance.liked_by.count()

    class Meta:
        model = Post
        # Liste de tous les champs qui peuvent être inclus dans une requête ou une réponse
        fields = ['id', 'author', 'body', 'edited', 'liked',
                  'likes_count', 'created', 'updated']
        # Les champs qui sont en lecture seule
        read_only_fields = ["edited"] 
