from rest_framework import status 
from core.fixtures.user import user 
from core.fixtures.post import post 
class TestPostViewSet: 
    endpoint = '/api/post/'


   # Teste la récupération d'une liste de posts
    def test_list(self, client, user, post):
        # Authentifie le client avec un utilisateur
        client.force_authenticate(user=user)
        # Fait une requête GET à l'endpoint correspondant à la liste de posts
        response = client.get(self.endpoint)
        # Vérifie que le code de réponse est 200 OK
        assert response.status_code == status.HTTP_200_OK
        # Vérifie que la réponse contient une clé "count" avec une valeur de 1
        assert response.data["count"] == 1

    # Teste la récupération d'un post spécifique avec son auteur
    def test_retrieve(self, client, user, post):
        # Authentifie le client avec un utilisateur
        client.force_authenticate(user=user)
        # Fait une requête GET à l'endpoint correspondant au post spécifique
        response = client.get(self.endpoint +
                            str(post.public_id) + "/")
        # Vérifie que le code de réponse est 200 OK
        assert response.status_code == status.HTTP_200_OK
        # Vérifie que la réponse contient une clé "id" avec une valeur égale à l'identifiant public du post
        assert response.data['id'] == post.public_id.hex
        # Vérifie que la réponse contient une clé "body" avec une valeur égale au corps du post
        assert response.data['body'] == post.body
        # Vérifie que la réponse contient une clé "author" avec une clé "id" ayant une valeur égale à l'identifiant public de l'auteur du post
        assert response.data['author']['id'] == post.author.public_id.hex

    # Teste la création d'un post
    def test_create(self, client, user): 
        # Authentifie le client avec un utilisateur
        client.force_authenticate(user=user) 
        # Prépare les données de test pour le corps et l'auteur du post
        data = { 
            "body": "Test Post Body", 
            "author": user.public_id.hex 
        } 
        # Envoie une requête POST à l'endpoint avec les données de test
        response = client.post(self.endpoint, data) 
        # Vérifie que la réponse est de code 201 CREATED et que les données du post sont correctes
        assert response.status_code == status.HTTP_201_CREATED 
        assert response.data['body'] == data['body'] 
        assert response.data['author']['id'] == user.public_id.hex 

        # Teste la création d'un post par un utilisateur anonyme
    def test_create_anonymous(self, client):
        data = { 
            "body": "Test Post Body", 
            "author": "test_user"
        } 
        response = client.post(self.endpoint, data) 
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Teste la mise à jour d'un post par un utilisateur anonyme
    def test_update_anonymous(self, client, post):
        data = { 
            "body": "Test Post Body", 
            "author": "test_user"
        } 
        response = client.put(self.endpoint + str(post.public_id) + "/", data) 
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Teste la suppression d'un post par un utilisateur anonyme
    def test_delete_anonymous(self, client, post):
        response = client.delete(self.endpoint + str(post.public_id) + "/") 
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

