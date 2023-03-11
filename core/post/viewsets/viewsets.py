# Import des modules nécessaires
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.abstrait.viewsets import AbstractViewSet
from core.post.models import Post
from core.post.serializers.serializers import PostSerializer
from rest_framework.decorators import action




# Définition d'un viewset pour la classe Post
class PostViewSet(AbstractViewSet):
    # Spécification des méthodes HTTP autorisées
    http_method_names = ('post', 'get','put','delete')
    # Spécification de la permission requise pour accéder au viewset
    permission_classes = (IsAuthenticated,)
    # Spécification du sérialiseur à utiliser pour la classe Post
    serializer_class = PostSerializer

    # Récupération de tous les objets de la classe Post
    def get_queryset(self):
        return Post.objects.all()

    # Récupération d'un objet spécifique de la classe Post à partir de son identifiant public
    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk'])
        # Vérification des permissions pour l'objet récupéré
        self.check_object_permissions(self.request, obj)
        return obj

    # Création d'un nouvel objet de la classe Post
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

     # Définir une action "like" pour ajouter un like à un post
   # Cette action requiert un HTTP POST request
    @action(methods=['post'], detail=True) 
    def like(self, request, *args, **kwargs): 
       
       # Récupérer le post à liker en utilisant la méthode get_object()
       post = self.get_object() 
       
       # Récupérer l'utilisateur qui a effectué la requête
       user = self.request.user 
       
       # Appeler la méthode like() de l'utilisateur pour ajouter un like au post
       user.like(post) 
       
       # Sérialiser le post en utilisant la classe de sérialisation associée à la vue
       serializer = self.serializer_class(post)
       return Response(serializer.data, status=status.HTTP_200_OK)


