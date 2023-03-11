# On importe les modèles de Django
from django.db import models

# On importe deux classes d'abstraction de modèles personnalisées définies ailleurs dans le projet
from core.abstrait.models import AbstractModel, AbstractManager

# On définit une nouvelle classe de gestionnaire de modèle appelée CommentManager qui hérite de la classe AbstractManager
class CommentManager(AbstractManager):
    pass

# On définit une nouvelle classe de modèle appelée Comment qui hérite de la classe AbstractModel
class Comment(AbstractModel):
    # On définit plusieurs champs de données
    post = models.ForeignKey("core_post.Post", on_delete=models.PROTECT)
    author = models.ForeignKey("core_user.User", on_delete=models.PROTECT)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    objects = CommentManager() # On utilise le gestionnaire de modèle CommentManager pour gérer les objets de modèle Comment

    # On définit une méthode qui renvoie le nom de l'auteur du commentaire pour l'affichage dans l'interface utilisateur
    def __str__(self):
        return self.author.name
