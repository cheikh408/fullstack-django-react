from core.auth.viewsets.login import LoginViewSet
from core.auth.viewsets.refresh import RefreshViewSet
from core.auth.viewsets.register import RegisterViewSet
from core.comment.viewsets.viewsets import CommentViewSet
from core.post.viewsets.viewsets import PostViewSet
from rest_framework import routers
from core.user.viewsets import UserViewSet
from rest_framework_nested import routers 


# On crée un routeur simple
router = routers.SimpleRouter()

# On enregistre la vue UserViewSet avec le nom 'user' et le basename 'user'
router.register(r'user', UserViewSet, basename='user')
router.register(r'auth/register', RegisterViewSet, basename='register')
router.register(r'auth/login', LoginViewSet,
    basename='auth-login')

router.register(r'auth/refresh', RefreshViewSet,
    basename='auth-refresh')    

router.register(r'post', PostViewSet,
    basename='post')

posts_router = routers.NestedSimpleRouter(router, r'post', lookup='post')
posts_router = routers.NestedSimpleRouter(router, r'post', lookup='post')
posts_router.register(r'comment', CommentViewSet, basename='post-comment')


# On définit les URL à utiliser avec le routeur
urlpatterns = [
   *router.urls,
   *posts_router.urls
]
