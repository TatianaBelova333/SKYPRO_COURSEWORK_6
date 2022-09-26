from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from ads.models import Ad, Comment
from ads.serializers import AdListSerializer, CommentSerializer, AdDetailSerializer, AdCreateSerializer, CommentCreateSerializer
from ads.filters import AdFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from ads.permissions import IsAdminOrAdOwner
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
        list=extend_schema(summary="Retrieves the list of all the comments to the ad specified by ad_id"),
        create=extend_schema(summary="Creates a new comment to the specified ad"),
        retrieve=extend_schema(summary="Retrieves the comment specified by its pk"),
        destroy=extend_schema(summary="Deletes the comment specified by its pk"),
        partial_update=extend_schema(summary="Updates the comment specified by its pk"),
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns a list of all the comments for
        the ad as determined by the ad_pk portion of the URL.
        """
        ad_id = self.kwargs['ad_pk']
        return self.queryset.filter(ad__id=ad_id)

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""

        if self.action in ('retrieve', 'create'):
            permission_classes = [IsAuthenticated]
        elif self.action in ('update', 'destroy', 'partial_update'):
            permission_classes = [IsAuthenticated, IsAdminOrAdOwner]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Returns the serializer class for each particular method"""

        if self.action == 'retrieve':
            return CommentSerializer
        elif self.action in ("create", "partial_update", "update"):
            return CommentCreateSerializer
        else:
            return CommentSerializer

    def perform_create(self, serializer):
        """Creates a comment for the ad specified by ad_pk """
        ad_id = self.kwargs['ad_pk']
        ad = get_object_or_404(Ad, id=ad_id)
        serializer.save(author=self.request.user, ad=ad)

    def perform_update(self, serializer):
        """Updates a comment for the ad specified by ad_pk """
        ad_id = self.kwargs['ad_pk']
        ad = get_object_or_404(Ad, id=ad_id)
        serializer.save(author=self.request.user, ad=ad)
