import pytest
from rest_framework import status
from core.fixtures.user import user


class TestAuthenticationViewSet:
    endpoint = "/api/auth/"
    @pytest.mark.django_db
    def test_login(self,client, user):
        # Arrange
        data = {
            "username": user.username,
            "password": "test_password"
        }


        # Act
        response = client.post(self.endpoint + "login/", data)

        # Assert
        assert response.status_code == 200
        assert response.data["access"]
        assert response.data["user"]["id"] == str(user.public_id)
        assert response.data["user"]["username"] == user.username
        assert response.data["user"]["email"] == user.email


    @pytest.mark.django_db 
    def test_register(self, client): 
        data = { 
            "username": "johndoe", 
            "email": "johndoe@yopmail.com", 
            "password": "test_password", 
            "first_name": "John", 
            "last_name": "Doe" 
        } 
        response = client.post(self.endpoint + "register/", data) 
        assert response.status_code == status.HTTP_201_CREATED 

    def test_refresh(self, client, user): 
        data = { 
            "username": user.username,
            "password": "test_password" 
        }
        response = client.post(self.endpoint + "login/", data) 
        assert response.status_code == status.HTTP_200_OK 
        data_refresh = { 
            "refresh": response.data['refresh'] 
        } 
        response = client.post(self.endpoint + "refresh/", data_refresh) 
        assert response.status_code == status.HTTP_200_OK 
        assert response.data['access']
    