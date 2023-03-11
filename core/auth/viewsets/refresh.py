from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import viewsets
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    # Définit les permissions pour autoriser tout le monde à accéder à cette vue
    permission_classes = (AllowAny,)
    # Définit les méthodes HTTP autorisées pour cette vue
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):
        # Crée une instance du sérialiseur de rafraîchissement de jeton
        serializer = self.get_serializer(data=request.data)
        try:
            # Vérifie si les données envoyées sont valides
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Si une erreur de jeton se produit, retourne une réponse d'erreur 401
            raise InvalidToken(e.args[0])
        # Si les données sont valides, renvoie une réponse avec les données validées et le code de statut 200 OK
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
