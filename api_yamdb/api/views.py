import uuid

from django.core.mail import EmailMessage, send_mail
from django.db import IntegrityError
from rest_framework import permissions, status, viewsets, filters
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status, viewsets

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


from users.models import User

from .permissions import AdminOnly, IsAdminOrReadOnly, AdminModeratorAuthorPermission
from .serializers import (SerializerNotAdmin, SerializerSignUp,
                          SerializerUsers, SerializerToken, ReviewSerializer, CommentSerializer,
                          CategorySerializer, GenreSerializer, TitleSerializer)
from .filters import TitlesFilter
from reviews.models import Review, Title, Comment, Category, Genre


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AdminModeratorAuthorPermission]

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_destroy(self, serializer):
        review_id = self.kwargs.get('pk')
        review = get_object_or_404(Review, pk=review_id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        super(ReviewViewSet, self).perform_update(serializer)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AdminModeratorAuthorPermission]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)

    def perform_destroy(self, serializer):
        comment_id = self.kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        super(CommentViewSet, self).perform_update(serializer)

