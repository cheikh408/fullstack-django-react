from rest_framework import serializers 
from rest_framework.exceptions import ValidationError 
from core.abstrait.serializers import AbstractSerializer 
from core.user.models import User 
from core.user.serializers import UserSerializer 
from core.comment.models import Comment
from core.post.models import Post



class CommentSerializer(AbstractSerializer):
    # Définir deux champs de liaison de clés étrangères en utilisant SlugRelatedField
    # pour associer chaque commentaire à un utilisateur et à une publication
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='public_id'
    )
    post = serializers.SlugRelatedField(
        queryset=Post.objects.all(), slug_field='public_id'
    )
    
    # Surcharge la méthode to_representation() pour personnaliser la représentation JSON
    # des objets Comment. Cette méthode est appelée lorsqu'un objet Comment doit être 
    # sérialisé en JSON.
    def to_representation(self, instance):
        # Appeler la méthode to_representation() de la classe parente pour obtenir une
        # représentation JSON initiale de l'objet Comment
        rep = super().to_representation(instance)
        
        # Récupérer l'utilisateur associé à chaque commentaire à partir de la clé publique
        # de l'utilisateur en utilisant la méthode get_object_by_public_id() définie sur le
        # modèle User
        author = User.objects.get_object_by_public_id(rep["author"])
        
        # Sérialiser l'utilisateur récupéré en utilisant le sérialiseur UserSerializer,
        # et remplacer la clé publique de l'utilisateur dans le dictionnaire Comment initial
        # par le dictionnaire sérialisé de l'utilisateur
        rep["author"] = UserSerializer(author).data
        
        # Retourner le dictionnaire modifié pour la sérialisation en JSON
        return rep
    
    class Meta:
        # Spécifier que le modèle Comment est utilisé pour la sérialisation
        model = Comment
        
        # Liste de tous les champs qui peuvent être inclus dans une requête ou une réponse
        fields = ['id', 'post', 'author', 'body', 'edited', 'created', 'updated']
        
        # Liste des champs qui ne peuvent être modifiés que par l'API, mais pas par les clients
        read_only_fields = ["edited"]