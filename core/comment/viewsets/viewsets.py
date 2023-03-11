from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import status
from core.abstrait.viewsets import AbstractViewSet
from core.comment.models import Comment
from core.comment.serializers.serializer import CommentSerializer
from core.auth.permissions import UserPermission

class CommentViewSet(AbstractViewSet):
    # Définition des méthodes HTTP autorisées
    http_method_names = ('post', 'get', 'put', 'delete')
    # Définition des permissions pour l'accès à ce viewset
    permission_classes = (UserPermission,)
    # Définition du serializer à utiliser pour les opérations de sérialisation/désérialisation
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        # Vérification si l'utilisateur est un superuser, si oui, récupération de tous les commentaires
        if self.request.user.is_superuser:
            return Comment.objects.all()
        # Récupération de l'ID de la publication
        post_pk = self.kwargs['post_pk']
        # Si l'ID n'existe pas, renvoyer une erreur 404
        if post_pk is None:
            raise Http404
        # Filtrage des commentaires liés à la publication correspondant à l'ID récupéré
        queryset = Comment.objects.filter(post__public_id=post_pk)
        return queryset
    

    def get_object(self):
        # Récupération de l'objet Comment correspondant à l'ID public fourni dans l'URL
        obj = Comment.objects.get_object_by_public_id(self.kwargs['pk'])
    # Vérification que l'utilisateur a les permissions nécessaires pour accéder à l'objet
        self.check_object_permissions(self.request, obj)
    # Renvoi de l'objet
        return obj
    
    def create(self, request, *args, **kwargs):
        # Obtention du serializer pour les données fournies dans la requête
         serializer = self.get_serializer(data=request.data)
    # Validation des données fournies
         serializer.is_valid(raise_exception=True)
    # Création de l'objet Comment
         self.perform_create(serializer)
    # Renvoi des données sérialisées de l'objet Comment créé avec un statut HTTP 201
         return Response(serializer.data, status=status.HTTP_201_CREATED)
