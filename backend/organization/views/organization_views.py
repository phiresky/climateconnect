from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from organization.serializers.organization import (
    OrganizationSerializer, OrganizationMinimalSerializer
)
from organization.models import Organization, OrganizationMember
from organization.permissions import OrganizationReadWritePermission
from climateconnect_api.models import Role
import logging
logger = logging.getLogger(__name__)


class ListOrganizationsAPIView(ListAPIView):
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    pagination_class = PageNumberPagination
    search_fields = ['url_slug']
    queryset = Organization.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return OrganizationSerializer

        return OrganizationMinimalSerializer


class CreateOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        required_params = ['name', 'team_members']
        for param in required_params:
            if param not in request.data:
                return Response({
                    'message': 'Required parameter missing: {}'.format(param)
                }, status=status.HTTP_400_BAD_REQUEST)

        organization, created = Organization.objects.get_or_create(name=request.data['name'])

        if created:
            organization.url_slug = organization.name.replace(" ", "") + str(organization.id)

            if 'image' in request.data:
                organization.image = request.data['image']
            if 'background_image' in request.data:
                organization.background_image = request.data['background_image']

            if 'parent_organization' in request.data:
                try:
                    parent_org = Organization.objects.get(id=int(request.data['parent_organization']))
                except Organization.DoesNotExist:
                    return Response({
                        'message': 'Parent organization not found.'
                    }, status=status.HTTP_404_NOT_FOUND)

                organization.parent_organization = parent_org

            if 'country' in request.data:
                organization.country = request.data['country']
            if 'state' in request.data:
                organization.state = request.data['state']
            if 'city' in request.data:
                organization.city = request.data['city']
            if 'short_description' in request.data:
                organization.short_description = request.data['short_description']
            organization.save()

            roles = Role.objects.all()
            for member in request.data['team_members']:
                user_role = roles.filter(id=int(member['permission_type_id'])).first()
                try:
                    user = User.objects.get(id=int(member['user_id']))
                except User.DoesNotExist:
                    logger.error("Passed user id {} does not exists".format(member['user_id']))
                    continue

                if user:
                    OrganizationMember.objects.create(
                        user=user, organization=organization, role=user_role
                    )
                    logger.info("Organization member created {}".format(user.id))

            return Response({
                'message': 'Organization {} successfully created'.format(organization.name)
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Organization with name {} already exists'.format(request.data['name'])
            }, status=status.HTTP_400_BAD_REQUEST)


class OrganizationAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [OrganizationReadWritePermission]
    serializer_class = OrganizationSerializer
    lookup_field = 'url_slug'

    def get_queryset(self):
        return Organization.objects.filter(url_slug=str(self.kwargs['url_slug']))

    def perform_update(self, serializer):
        serializer.save()
        return serializer

    def perform_destroy(self, instance):
        instance.delete()
        return "Organization successfully deleted."
