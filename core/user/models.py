
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
from core.abstrait.models import AbstractModel, AbstractManager



class UserManager(BaseUserManager, AbstractManager):
    

    def create_user(self, username, email, password=None, **kwargs):
        if not username:
            raise ValueError('Users must have a username.')
        if not email:
            raise ValueError('Users must have an email.')
        if not password:
            raise ValueError('Users must have a password.')
        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        user = self.create_user(username=username, email=email, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):

    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    posts_liked = models.ManyToManyField("core_post.Post", related_name="liked_by")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
    
    def __str__(self):
        return f"{self.email}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
 
    def like(self, post):
        """Ajoute un like au post si l'utilisateur ne l'a pas encore aimé"""
        # Utilise la méthode add() pour ajouter le post au set posts_liked de l'utilisateur
        # Si le post a déjà été ajouté, il ne sera pas ajouté une deuxième fois
        return self.posts_liked.add(post)

    def remove_like(self, post):
        """Supprime un like d'un post"""
        # Utilise la méthode remove() pour supprimer le post du set posts_liked de l'utilisateur
        # Si le post n'a pas été aimé précédemment, il ne sera pas supprimé
        return self.posts_liked.remove(post)

    def has_liked(self, post):
        """Vérifie si l'utilisateur a aimé le post"""
        # Utilise la méthode filter() pour filtrer le set posts_liked en fonction du pk (primary key) du post
        # La méthode exists() vérifie si un objet correspondant à la requête existe dans la base de données
        # Retourne True si un objet existe, sinon False
        return self.posts_liked.filter(pk=post.pk).exists()

    

    





