from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


# Create your views here.
class TestApiView(APIView):
    """Test API View"""
    serializer_class = serializers.TestSerializer

    def get(self, request, format=None):
        ret_json = {
            "Message": "Test get api view django",
            "Status": 200
        }

        return Response({
            "Message": "Hello user!",
            "ret_json": ret_json
        })

    def post(self, request):
        """get posted data and say hello"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({
                'Message': message
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )


class TestViewSet(viewsets.ViewSet):
    """Test API ViewSets"""
    serializer_class = serializers.TestSerializer

    def list(self, request):
        ret_json = {
            'Use actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provide more functionality with less code'
        }
        return Response({
            'Message': ret_json
        })

    def create(self, request):
        # Create new Hello Message
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({
                'Message': message
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileViewSet(viewsets.ModelViewSet):
    # Handle creating and updating profiles
    """Provide query set to model ViewSet, so we know which objects
    are going to be managed throug this ViewSet"""
    serializer_class = serializers.UserProfileSerial
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')
