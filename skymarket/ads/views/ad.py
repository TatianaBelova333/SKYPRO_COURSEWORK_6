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
        list=extend_schema(summary="Retrieves the list of all the ads"),
        create=extend_schema(summary="Creates a new ad"),
        retrieve=extend_schema(summary="Retrieves the ad specified by its pk"),
        destroy=extend_schema(summary="Deletes the ad specified by its pk"),
        partial_update=extend_schema(summary="Updates the ad specified by its pk"),
        list_user_ads=extend_schema(summary="Retrieves the list of the user's ads"),
)
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter
    serializer_class = AdListSerializer
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_serializer_class(self):
        """Returns the serializer class for each particular method"""
        if self.action == 'retrieve':
            return AdDetailSerializer
        elif self.action in ("create", "partial_update", "update"):
            return AdCreateSerializer
        else:
            return AdListSerializer

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""
        if self.action in ('retrieve', 'create'):
            permission_classes = [IsAuthenticated]
        elif self.action in ('update', 'destroy', 'partial_update'):
            permission_classes = [IsAuthenticated, IsAdminOrAdOwner]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_user:
            serializer.save(author=self.request.user)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, IsAdminOrAdOwner],
            url_path='me', url_name='list_user_ads')
    def list_user_ads(self, request, pk=None):
        """Returns a list of all the ads posted by the currently authenticated user."""
        user = self.request.user
        self.queryset = user.ads
        return self.list(request, pk=None)
