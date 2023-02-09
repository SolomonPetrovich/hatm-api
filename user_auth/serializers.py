from rest_framework import serializers
from .models import CustomUser as User
from hatm.serializers import JuzSerializer
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    juz_set = JuzSerializer(many=True, read_only=True)
    email = serializers.ReadOnlyField()
    hatms_created = serializers.ReadOnlyField()
    active_hatms = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('email', 'nickname', 'juz_set', 'hatms_created', 'active_hatms')