from core.abstrait.viewsets import AbstractViewSet
from rest_framework.permissions import IsAuthenticated
from core.user.serializers import UserSerializer
from core.user.models import User

class UserViewSet(AbstractViewSet):
    # On spécifie les méthodes HTTP autorisées
    http_method_names = ('patch', 'get')
    # On autorise les utilisateurs authenfiés à accéder à la vue
    permission_classes = (IsAuthenticated,)
    # On utilise le serializer UserSerializer pour sérialiser/désérialiser les instances User
    serializer_class = UserSerializer
    
    def get_queryset(self):
        # Si l'utilisateur est un superutilisateur, il peut voir tous les utilisateurs
        if self.request.user.is_superuser:
            return User.objects.all()
        # Sinon, il ne peut voir que les utilisateurs qui ne sont pas des superutilisateurs
        return User.objects.exclude(is_superuser=True)
    
    def get_object(self):
        # On récupère l'utilisateur correspondant à la clé publique spécifiée dans l'URL
        obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
        # On vérifie si l'utilisateur a les permissions nécessaires pour accéder à cet objet
        self.check_object_permissions(self.request, obj)
        # On retourne l'objet utilisateur
        return obj
