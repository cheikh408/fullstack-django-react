from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from core.auth.serializers import LoginSerializer

class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        try:
            # Vérifie si les données envoyées sont valides
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Si une exception TokenError est levée, on la traite et on renvoie une réponse d'erreur
            raise InvalidToken(e.args[0])
        
        # Si les données sont valides, on renvoie une réponse contenant les données validées et le code de statut HTTP 200
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
