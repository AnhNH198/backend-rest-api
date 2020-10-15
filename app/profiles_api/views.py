from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profiles_api import serializers


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
