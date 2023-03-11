from rest_framework.permissions import BasePermission, SAFE_METHODS



class UserPermission(BasePermission):
    # Vérifie si l'utilisateur a la permission d'accéder à une instance spécifique de la vue
    def has_object_permission(self, request, view, obj):
        # Si l'utilisateur est anonyme (non connecté)
        if request.user.is_anonymous:
            # Autoriser l'accès uniquement aux méthodes de requête sûres (par exemple, GET ou HEAD)
            return request.method in SAFE_METHODS
        # Si l'utilisateur est connecté et que la vue est "post"
        if view.basename in ["post"]:
            # Autoriser l'accès uniquement si l'utilisateur est authentifié
            return bool(request.user and request.user.is_authenticated)
        # Dans tous les autres cas, refuser l'accès
        return False

    # Vérifie si l'utilisateur a la permission d'accéder à la vue
    def has_permission(self, request, view):
        # Si la vue est "post"
        if view.basename in ["post"]:
            # Si l'utilisateur est anonyme (non connecté)
            if request.user.is_anonymous:
                # Autoriser l'accès uniquement aux méthodes de requête sûres (par exemple, GET ou HEAD)
                return request.method in SAFE_METHODS
            # Si l'utilisateur est connecté, autoriser l'accès
            return bool(request.user and request.user.is_authenticated)
        # Dans tous les autres cas, refuser l'accès
        return False
