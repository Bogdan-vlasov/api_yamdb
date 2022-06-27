from django.urls import include, path
from rest_framework.routers import SimpleRouter

from rest_framework import routers
from rest_framework.authtoken import views

from api.views import (

    UsersViewSet,
    APIGetToken,
    APISignup,
    ReviewViewSet,
    CommentViewSet,
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet
)
app_name = 'api'
router = SimpleRouter()

router.register(
    'users',
    UsersViewSet,
    basename='users'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

router.register('titles', TitleViewSet, basename='title')

router.register('categories', CategoryViewSet,
                basename='category')

router.register('genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]