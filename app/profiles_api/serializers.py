from rest_framework import serializers

from profiles_api import models


class TestSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10, required=True)


class MaHoa(serializers.Serializer):
    văn_Bản = serializers.CharField(required=True)
    key = serializers.IntegerField(required=True)


class GiaiMa(serializers.Serializer):
    văn_Bản = serializers.CharField(required=True)
    key = serializers.IntegerField(required=True)


class MaHoaRSA(serializers.Serializer):
    văn_Bản = serializers.CharField(required=True)
    p_value = serializers.IntegerField(required=True)
    q_value = serializers.IntegerField(required=True)


class GiaiMaRSA(serializers.Serializer):
    d = serializers.IntegerField(required=True)
    n = serializers.IntegerField(required=True)
    văn_Bản = serializers.CharField(required=True)


class UserProfileSerial(serializers.ModelSerializer):
    """Serializers an user profile object"""

    """Use Meta class to point to specify project in this case is
    UserProfile in model"""
    class Meta:
        model = models.UserProfile
        """Specify a list of field in model that we want to manage through our
        serialization.
        This is the list of all field that you want to either make accessible
        in our API or you want to create new models with serializers
        """
        fields = ('id', 'email', 'name', 'password')
        """The special field is password need extra keyword
        """
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user


class UserProfileFeedSerial(serializers.ModelSerializer):
    # class Meta:
    class Meta:
        # Declare Model to use
        model = models.ProfileFeedItem
        # Declare fields = ()
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        # extra_kwargs
        extra_kwargs = {
            'user_profile': {
                'read_only': True
            }
        }
