from rest_framework import serializers
from .models import CustomUser as User
from hatm.serializers import JuzSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from . import google
from .register import register_social_user
from core.settings import SOCIAL_AUTH_GOOGLE_OAUTH2_KEY


class UserSerializer(serializers.HyperlinkedModelSerializer):
    juz_set = JuzSerializer(many=True, read_only=True)
    email = serializers.ReadOnlyField()
    hatms_created = serializers.ReadOnlyField()
    active_hatms = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('email', 'nickname', 'juz_set', 'hatms_created', 'active_hatms')


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        # if user_data['aud'] != SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:
        #     raise AuthenticationFailed('oops, who are you?')


        email = user_data['email']
        provider = 'google'

        return register_social_user(
            provider=provider, email=email)
